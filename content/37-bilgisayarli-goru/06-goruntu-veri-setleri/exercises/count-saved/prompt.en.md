`count_saved(n, seed)` should save the `make_shapes(n, seed=seed)` pictures in a
temporary folder (`tempfile.TemporaryDirectory()`) in the lesson's layout
(`root/class/NNN.png`, grey, `uint8`) and, before the folder is removed,
return the number of `.png` files in each class folder in `SHAPES` order, as a
list.

**Expected output:**

```
[11, 8, 11]
[4, 4, 4]
```
