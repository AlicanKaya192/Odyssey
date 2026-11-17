`lost_objects(scene, S, size)` should return how many of a scene's
`[x1, y1, x2, y2, class]` boxes are lost because their centre falls into the
same cell as an earlier object (grid `S × S`, picture `size` pixels).

**Expected output:**

```
0
0
```
