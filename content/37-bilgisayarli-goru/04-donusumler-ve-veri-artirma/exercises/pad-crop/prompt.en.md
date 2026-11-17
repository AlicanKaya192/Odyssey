`pad_crop(img, padding, top, left)` should do what `RandomCrop` does, without
randomness: add `padding` zeros on every side of the picture (`F.pad`), then
cut a piece the same size as the picture starting at the `(top, left)`
corner. The result is a nested list.

**Expected output:**

```
[[0, 0], [0, 1]]
[[1, 2], [3, 4]]
[[4, 0], [0, 0]]
```
