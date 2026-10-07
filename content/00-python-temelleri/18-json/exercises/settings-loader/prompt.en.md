A program's settings are in `DEFAULTS`; the user can change some of them with
a JSON file. Two files have been placed next to your code:

- `good.json`: `{"theme": "light", "font_size": 14}`
- `broken.json`: broken JSON with an extra comma at the end

There is **no** file called `missing.json`.

**What to do:**

Write the function `load_settings(path)`:

1. Take a **copy** of the defaults with `settings = DEFAULTS.copy()`.
2. Open the file and read it with `json.load`; write the value of every key
   in the file into `settings` (those not in the file stay default).
3. If the file is missing (`FileNotFoundError`) or broken
   (`json.JSONDecodeError`), return the copy of the defaults unchanged.
4. Return `settings`.

Then call the function with `good.json`, `missing.json` and `broken.json`,
in order; print the `theme`, `font_size` and `language` of each result on
one line.

**Expected output:**

```text
light 14 en
dark 12 en
dark 12 en
```

Why a copy? If you write `settings = DEFAULTS`, both are **the same**
dictionary; loading `good.json` changes `DEFAULTS` too, and later calls no
longer see the real defaults.
