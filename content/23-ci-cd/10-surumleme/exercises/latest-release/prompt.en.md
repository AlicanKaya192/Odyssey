Write the function `latest_release(tags)`. It should take a list of git tags and return the tag of the **newest stable version**; `None` if there is none.

- A stable version tag starts with `v`, followed by **exactly three parts** separated by dots, and each part is only digits (`v1.10.0`). `v2.0.0rc1`, `v1.10` and `nightly` do not count.
- Versions are compared **as numbers**: `v1.10.0` is newer than `v1.9.3`.

`part.isdigit()` tells whether a text is made only of digits.

**Expected output:**

```
v1.10.0
None
v0.10.0
```
