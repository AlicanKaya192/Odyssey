There is an `app` folder next to your file: `main.py`, `utils.py`,
`cache.tmp`, `temp/output.txt`, `data/config.json`.

Write the function `clean_release(src, dst)`: copy `src` to `dst`, but skip
`*.tmp` files and the `temp` folder; if `dst` already exists, copy over it.
At the end return the relative, `/`-separated paths of the **files** in `dst`
as a sorted list.

**Expected output:**

```
data/config.json
main.py
utils.py
```
