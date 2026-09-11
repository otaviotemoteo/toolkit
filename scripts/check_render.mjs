// The point a layer turns on must stay put, at every size the page renders at.
//
// This is the one property the whole hero rests on. The head is joined to the
// body by nothing but a shared pixel column at the base of the neck: if the
// pivot moves, the neck leaves the collar and the character comes apart. A
// rotation about the pivot cannot move the pivot, so the only way it drifts is
// if the origin handed to CSS is not actually the pivot.
//
// That is exactly what happened, and it survived review because the error
// scales with the element. At file resolution the origin was right. In a 92px
// preview cell the same number sat almost three head heights below the chin and
// the neck swung 21px clear of the collar. See
// docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md.
//
// The check imports originFor from preview/hero.js rather than restating its
// arithmetic, on the same reasoning as scripts/check_anchors.py: a check that
// carries its own copy of the thing it checks stops checking the moment the
// original is edited.
//
//     node scripts/check_render.mjs
//     node scripts/check_render.mjs <hero.js> <scene.json>

import { readFile } from "node:fs/promises";
import { glob } from "node:fs/promises";
import { resolve, dirname, relative } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

// Sizes a preview actually renders at: a grid cell, the measured hero, a wide
// hero, and one absurdly small, because the failure got worse as it got smaller.
const WIDTHS = [40, 92, 282, 1102];
const TOLERANCE = 0.01; // css px

function parseOrigin(origin, w, h) {
  const parts = String(origin).trim().split(/\s+/);
  if (parts.length !== 2) return null;
  const axis = [w, h];
  return parts.map((part, i) => {
    if (part.endsWith("%")) return (parseFloat(part) / 100) * axis[i];
    if (part.endsWith("px")) return parseFloat(part);
    return NaN;
  });
}

function problems(scene, originFor) {
  const found = [];
  const ch = scene.character;
  const lean = (scene.limits?.lean_deg ?? 0) * Math.PI / 180;

  for (const [joint, pivot] of Object.entries(ch.pivots ?? {})) {
    // Only the layers the renderer actually turns. A static layer is never
    // given an origin, and asserting one for it would be the check inventing a
    // requirement the hero does not have.
    for (const name of TURNS_WITH?.[joint] ?? [joint]) {
      const L = ch.layers[name];
      if (!L) continue;

      for (const w of WIDTHS) {
        const h = w * (L.height / ch.file_size[0]);
        const origin = parseOrigin(originFor(scene, name, joint), w, h);
        if (!origin || origin.some(Number.isNaN)) {
          found.push([
            `origin for ${name}/${joint} is ${JSON.stringify(originFor(scene, name, joint))}`,
            "css cannot resolve it, so the layer turns about its own centre",
            "return two lengths, in units that scale with the element",
          ]);
          break;
        }
        // Where the pivot itself lands inside an element of this size.
        const want = [
          (pivot[0] / ch.file_size[0]) * w,
          ((pivot[1] - L.top) / L.height) * h,
        ];
        const off = [origin[0] - want[0], origin[1] - want[1]];
        if (Math.abs(off[0]) <= TOLERANCE && Math.abs(off[1]) <= TOLERANCE) continue;

        // Restate the miss as the thing anyone would see: how far the joint
        // slides when the layer turns by the angle the scene actually allows.
        const r = Math.hypot(off[0], off[1]);
        const drift = 2 * r * Math.sin(lean / 2);
        found.push([
          `layer ${name} turns about a point ${off[0].toFixed(1)}px across and ` +
            `${off[1].toFixed(1)}px down from its pivot, when rendered ${w}px wide`,
          `at ${scene.limits?.lean_deg ?? 0} degrees the joint slides ` +
            `${drift.toFixed(1)}px, and a joint that moves is a seam that opens`,
          "express the origin as a share of the element's own box, not in the " +
            "pixels of the file it was measured in",
        ]);
        break; // one report per layer is enough; the rest say the same thing
      }
    }
  }
  return found;
}

const [heroArg, sceneArg] = process.argv.slice(2);
const heroPath = resolve(ROOT, heroArg ?? "preview/hero.js");
const { originFor, TURNS_WITH } = await import(pathToFileURL(heroPath).href);

if (typeof originFor !== "function") {
  console.error(`check_render: ${relative(ROOT, heroPath)} exports no originFor`);
  process.exit(1);
}

const scenes = sceneArg
  ? [resolve(ROOT, sceneArg)]
  : (await Array.fromAsync(glob("briefs/*/approved/scene/scene.json", { cwd: ROOT })))
      .sort()
      .map((p) => resolve(ROOT, p));

if (!scenes.length) {
  console.error("check_render: no scene manifests found");
  process.exit(2);
}

let failed = 0;
for (const path of scenes) {
  const scene = JSON.parse(await readFile(path, "utf8"));
  const found = problems(scene, originFor);
  const rel = relative(ROOT, path);
  if (!found.length) {
    console.log(`ok    ${rel}`);
    continue;
  }
  failed++;
  for (const [what, why, fix] of found) {
    console.log(`FAIL  ${rel}`);
    console.log(`      what: ${what}`);
    console.log(`      why:  ${why}`);
    console.log(`      fix:  ${fix}`);
  }
}

if (failed) {
  console.log(`\ncheck_render: ${failed} of ${scenes.length} manifests failed`);
  process.exit(1);
}
// The puppet has its own runtime and its own manifest, and the same rule: a
// pivot written in the drawing's pixels is a pivot at one size only.
const rigs = (await Array.fromAsync(glob("briefs/*/approved/puppet/rig.json", { cwd: ROOT })))
  .sort()
  .map((p) => resolve(ROOT, p));
if (rigs.length) {
  const puppet = await import(pathToFileURL(resolve(ROOT, "preview/puppet.js")).href);
  for (const path of rigs) {
    const rig = JSON.parse(await readFile(path, "utf8"));
    const [cw, ch] = rig.canvas;
    for (const [name, pivot] of Object.entries(rig.pivots ?? {})) {
      for (const w of WIDTHS) {
        const h = w * (ch / cw);
        const got = parseOrigin(puppet.originFor(rig, name), w, h);
        const want = [(pivot[0] / cw) * w, (pivot[1] / ch) * h];
        if (Math.abs(got[0] - want[0]) > TOLERANCE || Math.abs(got[1] - want[1]) > TOLERANCE) {
          console.log(`FAIL  ${relative(ROOT, path)}`);
          console.log(`      what: joint ${name} turns off its pivot at ${w}px wide`);
          console.log("      why:  a hip that moves tears the trouser off the body");
          console.log("      fix:  express the origin as a share of the element's box");
          failed++;
        }
      }
    }
    console.log(`ok    ${relative(ROOT, path)}`);
  }
}

if (failed) {
  console.log(`\ncheck_render: ${failed} failure(s)`);
  process.exit(1);
}
console.log(`check_render: ${scenes.length + rigs.length} manifest(s) ok at ${WIDTHS.length} render sizes`);
