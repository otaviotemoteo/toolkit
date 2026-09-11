// Broken on purpose. This is the origin preview/hero.js shipped with, verbatim:
// the pivot written in the pixels of the file it was measured in.
//
// It is correct at exactly one render size and wrong everywhere else, which is
// why it passed review. If scripts/check_render.mjs ever accepts this file, the
// check has stopped testing anything. See
// docs/solutions/a-pivot-in-pixels-is-a-pivot-at-one-size.md.

export const TURNS_WITH = { head: ["head", "eyes"] };

export function originFor(scene, name, joint) {
  const ch = scene.character;
  const L = ch.layers[name];
  const pivot = ch.pivots[joint];
  return `${pivot[0]}px ${pivot[1] - L.top}px`;
}
