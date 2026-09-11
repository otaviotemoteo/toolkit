// A walking figure, from one drawing.
//
// Every state is the same three files. The legs turn about the hip and the body
// rises and falls; nothing here is generated, and there is no frame sequence to
// store, so five seconds of walking costs exactly what one second costs.
//
// Distance drives the cycle, not time. A walk whose stride is tied to the clock
// slides its feet the moment the figure moves at any other speed, and this
// figure is driven by scroll, whose speed is the reader's. Tying the phase to
// how far he has travelled means a footfall always happens after the same
// distance, which is what makes a walk read as walking rather than as legs
// waving. `period_px` in the rig is that distance.

export function originFor(rig, name) {
  // The same rule the hero learned the hard way: a pivot is a point in the
  // drawing's own pixels, and a layer on the page is an <img> that CSS scales.
  // Expressed as a share of the element's own box it survives any render size.
  // See docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md.
  const [cw, ch] = rig.canvas;
  const p = rig.pivots[name];
  if (!p) return "50% 50%";
  return `${(p[0] / cw) * 100}% ${(p[1] / ch) * 100}%`;
}

export async function mountPuppet(root, rigUrl) {
  const rig = await fetch(rigUrl).then((r) => r.json());
  const base = rigUrl.replace(/[^/]*$/, "");
  const [cw, ch] = rig.canvas;

  root.style.cssText +=
    `position:absolute;aspect-ratio:${cw}/${ch};will-change:transform`;

  const el = {};
  for (const name of rig.draw_order) {
    const img = document.createElement("img");
    img.src = base + rig.layers[name].file;
    img.style.cssText =
      "position:absolute;inset:0;width:100%;pointer-events:none;user-select:none";
    img.style.transformOrigin = originFor(rig, name);
    if (rig.pivots[name]) img.style.willChange = "transform";
    el[name] = img;
    root.appendChild(img);
  }

  const w = rig.walk;
  let last = "";

  /** Place him x px along his own travel, in the units of the parent box. */
  function setDistance(px) {
    const phase = (px / w.period_px) * Math.PI * 2;
    const swing = Math.sin(phase);
    const t = {};
    for (const [joint, dir] of Object.entries(w.joints)) {
      t[joint] = `rotate(${swing * dir * w.swing_deg}deg)`;
    }
    // The body rises twice per stride, at each passing position, which is what
    // stops a cut-out walk reading as a figure gliding on rails.
    const bob = -Math.abs(Math.cos(phase)) * w.bob_px;
    const key = px.toFixed(1);
    if (key === last) return;
    last = key;
    // A percentage translate resolves against the element's own box, so the
    // bob keeps its proportion at any size, for the same reason the origins do.
    root.style.transform = `translateY(${(bob / ch) * 100}%)`;
    for (const [name, value] of Object.entries(t)) {
      if (el[name]) el[name].style.transform = value;
    }
  }

  return { rig, setDistance, layers: el };
}
