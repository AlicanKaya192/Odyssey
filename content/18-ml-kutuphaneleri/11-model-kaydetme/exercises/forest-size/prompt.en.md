`forest_size(level)` should save the forest with `compress=level` and return the
file size in KB (`// 1024`). The starter code does not use `level`.

The size of the compressed file differs by a few KB with the compression
library Python uses (Python on Windows uses zlib-ng, on macOS zlib). So the
lines below check the uncompressed size exactly and whether the compressed
one is smaller than a third of it.

**Expected output:**

```
626
True
```
