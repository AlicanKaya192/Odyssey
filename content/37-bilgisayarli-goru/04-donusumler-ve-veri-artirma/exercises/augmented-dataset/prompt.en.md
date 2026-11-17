Complete the `__len__` and `__getitem__` methods of the `Shapes` class:
`__len__` should give the number of examples; `__getitem__(i)` should apply
the transform to the i-th picture if one was given (`transform` is not
`None`) and return `(picture, label)`.

**Expected output:**

```
20 20
(1, 16, 16) True
True False
```
