Complete the `Version` class: split text like `"1.10.2"` at the dots into
the tuple `self.parts` (`int`), let `__eq__` and `__lt__` compare these
tuples, and decorate the class with **`@total_ordering`**. Then let
`sort_versions(texts)` return the texts sorted in version order: `"1.2"`
comes before `"1.10"`.

**Expected output:**

```
['0.9', '1.2', '1.2.1', '1.10']
True
```
