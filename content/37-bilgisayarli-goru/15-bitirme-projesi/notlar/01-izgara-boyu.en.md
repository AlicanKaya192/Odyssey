In the capstone, 87 of the 1232 objects were lost because they shared a cell.
Does a finer grid reduce this? We can count it just by looking at the data
(no model needed):

```python
from dl_data import make_scenes

images, boxes, masks = make_scenes(600, size=32, seed=7)


def lost_objects(grid):
    cell = 32 / grid
    lost = 0
    for scene in boxes:
        taken = set()
        for x1, y1, x2, y2, label in scene:
            key = (int((y1 + y2) / 2 // cell), int((x1 + x2) / 2 // cell))
            lost += key in taken
            taken.add(key)
    return lost


for grid in (2, 4, 8, 16):
    print(grid, grid * grid, lost_objects(grid))
```

```text
2 4 198
4 16 87
8 64 25
16 256 9
```

- On a 2 × 2 grid 198 objects are lost, on 16 × 16 only 9.
- But a fine grid has a price too: on 16 × 16 very few of the 256 cells hold
  an object; the objectness loss is spent almost entirely on learning to say
  "there is no object here". Each cell also sees a smaller part of the
  picture.
- Real detectors combine two ways: several **anchors** per cell (the note in
  the YOLO Logic section) and **grids at several scales** (big objects on a
  coarse grid, small ones on a fine grid).
