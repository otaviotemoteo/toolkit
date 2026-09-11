// The hero motion primitive.
//
// The body, the desk and everything on it never move: they are the same pixels
// in every state, which is the acceptance criterion the whole approach exists
// to satisfy. See briefs/hero-character/motion.md.
//
// What moves is the head, which carries the neck with it, and the eyes. There is
// one joint, at the base of the neck where the collar is. A second joint was
// specified and removed: two raster layers cut from one flat drawing share the
// same pixels in their overlap, and showing those pixels at two different
// angles ghosted the jaw. Exclusive content per layer is the rule that replaced
// it, and one joint is what a single flat drawing can actually support.
//
// Nothing here generates anything. Every state is the same four files.

// Which layers turn on which joint. The eyes turn on the head's joint because
// they are part of the face; the body and the plate turn on nothing. Exported
// so scripts/check_render.mjs checks the layers that actually move, rather than
// a list it keeps privately and that stops matching the day this one changes.
export const TURNS_WITH = { head: ["head", "eyes"] };

// Where a layer turns, as a CSS transform-origin.
//
// The pivot is a point in the character's own pixel space, but the layer on the
// page is an <img> that CSS scales to whatever width the container gives it. An
// origin written in those pixels is correct at exactly one render size and
// silently wrong at every other, and being wrong costs nothing visible until it
// costs everything: at file resolution the head turned on its neck, and in a
// 92px preview cell the same number put the pivot almost three head heights
// below the chin, so the neck swung 21px clear of the collar.
//
// A percentage is the same point at every size, because the browser measures it
// against the element's own box rather than against a number we remembered from
// a file. See docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md.
//
// Exported because scripts/check_render.mjs tests this function rather than a
// copy of its arithmetic: a check that reimplements what it checks only proves
// the two agreed on the day they were written.
export function originFor(scene, name, joint) {
  const ch = scene.character;
  const L = ch.layers[name];
  const pivot = ch.pivots[joint];
  return `${(pivot[0] / ch.file_size[0]) * 100}% ` +
         `${((pivot[1] - L.top) / L.height) * 100}%`;
}

export async function mountHero(root, sceneUrl) {
  const scene = await fetch(sceneUrl).then((r) => r.json());
  const base = sceneUrl.replace(/[^/]*$/, "");
  const [cw, ch] = scene.canvas;
  const ch_ = scene.character;

  root.style.cssText +=
    `position:relative;aspect-ratio:${cw}/${ch};background:${scene.paper};overflow:hidden`;

  const px = (v) => `${(v / cw) * 100}%`;
  const img = (file, x, y, w) => {
    const el = document.createElement("img");
    el.src = base + file;
    el.style.cssText =
      `position:absolute;left:${px(x)};top:${px(y)};width:${px(w)};` +
      `image-rendering:auto;pointer-events:none;user-select:none`;
    return el;
  };

  root.appendChild(img(scene.plate.file, scene.plate.x, scene.plate.y, 750));

  // Each character layer is drawn at the same place as every other one: the
  // layer files are full-width crops, so their own top offset positions them.
  const s = ch_.scale;
  const layerEl = {};
  for (const name of ch_.draw_order) {
    const L = ch_.layers[name];
    const el = img(L.file, ch_.x, ch_.y + L.top * s, ch_.file_size[0] * s);
    layerEl[name] = el;
    root.appendChild(el);
  }

  for (const name of TURNS_WITH.head) {
    if (!layerEl[name]) continue;
    layerEl[name].style.transformOrigin = originFor(scene, name, "head");
    layerEl[name].style.willChange = "transform";
  }

  const lim = scene.limits;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const coarse = matchMedia("(pointer: coarse)").matches;

  let tx = 0, ty = 0;        // target, -1..1
  let cx = 0, cy = 0;        // current, smoothed
  let raf = 0, last = "";

  function apply() {
    // The head only rotates. It was given a small sideways translation at first
    // and that broke the join: rotation about the pivot leaves the pivot exactly
    // where it was, so the neck stays continuous with the collar, while any
    // translation slides the whole head against a body that did not move and
    // opens a step across the neck. Expression comes from the eyes instead.
    const lean = cx * lim.lean_deg;
    const t = {
      head: `rotate(${lean}deg)`,
      eyes: `rotate(${lean}deg) translate(${cx * lim.pupil_px}px, ` +
            `${cy * lim.pupil_py}px)`,
    };
    const key = JSON.stringify(t);
    if (key === last) return;          // one write per frame, and only on change
    last = key;
    for (const [name, value] of Object.entries(t)) {
      if (layerEl[name]) layerEl[name].style.transform = value;
    }
  }

  function tick() {
    const k = lim.smoothing;
    cx += (tx - cx) * k;
    cy += (ty - cy) * k;
    apply();
    if (Math.abs(tx - cx) > 0.001 || Math.abs(ty - cy) > 0.001) {
      raf = requestAnimationFrame(tick);
    } else {
      raf = 0;
    }
  }

  function aim(x, y) {
    if (still || coarse) return;
    tx = Math.max(-1, Math.min(1, x));
    ty = Math.max(-1, Math.min(1, y));
    if (!raf) raf = requestAnimationFrame(tick);
  }

  root.addEventListener("pointermove", (e) => {
    const r = root.getBoundingClientRect();
    // Measured from the head, not from the middle of the box, so he looks at
    // the cursor rather than at a point that happens to be near it.
    const hx = r.left + r.width * ((ch_.x + ch_.pivots.head[0] * s) / cw);
    const hy = r.top + r.height * ((ch_.y + ch_.pivots.head[1] * s) / ch);
    aim((e.clientX - hx) / (r.width * 0.5), (e.clientY - hy) / (r.height * 0.5));
  });
  root.addEventListener("pointerleave", () => aim(0, 0));

  return { aim, scene, layers: layerEl };
}
