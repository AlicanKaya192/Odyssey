Write the `Version` dataclass with `frozen=True, order=True`: the fields
are `major`, `minor`, `patch` (all `int`). Let `newest(texts)` build
`Version`s from texts like `"1.10.0"` and return the largest one (`max`) as
text in the same `"1.10.0"` form.

**Expected output:**

```
1.10.0
0.1.0
```
