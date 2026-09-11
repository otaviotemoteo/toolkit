# Broken scene manifest

Four faults in one file, one per rule in `scripts/check_scene.py`:

- `plate.png`, `body.png` and `head.png` do not exist
- `draw_order` lists `body` and forgets `head`, so the head would never draw
- the head's pivot is at y=60, outside the head layer, which spans 0..30
- `body` starts at y=10, above the pivot, so static pixels would show from
  behind the head as it turns

Each of these has happened, and the whole sequence is in
`docs/solutions/two-raster-layers-cannot-share-a-pixel.md`. The pivot and the body cut were both got wrong
while building the hero, and the missing file is what a rename does.
