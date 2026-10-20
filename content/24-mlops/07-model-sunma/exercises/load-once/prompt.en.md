`read_model()` in `store.py` reads the model from disk and counts every call (`reads["count"]`). Write the function `get_model()`:

- On the first call it should read the model with `read_model()` and put it into the module-level variable `_model`.
- On later calls it should return the same object without reading the disk.

After five requests the disk should have been read only **once**.

**Expected output:**

```
reads: 1
same object: True
version: 3
```
