Write the function `pick_cache(key, restore_keys, saved)`. `saved` is the list of stored caches; each one is `[name, created_minute]`, **in no order**.

- If one is named exactly `key`: `"hit: " + name`
- Otherwise try the prefixes in `restore_keys` in order; among the ones starting with a prefix, find the **newest** (the largest created minute): `"partial: " + name`
- If there is none: `"miss"`

**Expected output:**

```
hit: pip-Linux-aaaa
partial: pip-Linux-cccc
partial: pip-Linux-cccc
miss
```
