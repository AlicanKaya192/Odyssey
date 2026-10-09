## string

| Name | Contents |
|---|---|
| `ascii_lowercase` / `ascii_uppercase` | a–z / A–Z |
| `ascii_letters` | both |
| `digits` | 0–9 |
| `punctuation` | `!"#$%&'()*+,-./:;<=>?@[\]^_` and the rest |
| `whitespace` | space, tab, line break |
| `Template("...$name...")` | `substitute`, `safe_substitute` |

Deleting: `text.translate(str.maketrans("", "", string.punctuation))`.

## textwrap

| Function | What it does |
|---|---|
| `wrap(t, width=40)` | a list of lines |
| `fill(t, width=40)` | the lines joined into one text |
| `shorten(t, width=40, placeholder="...")` | shorten at a word boundary |
| `indent(t, "> ")` | a prefix on every line |
| `dedent(t)` | remove the common leading whitespace |

## difflib

| Function | What it gives |
|---|---|
| `SequenceMatcher(None, a, b).ratio()` | similarity 0–1 |
| `get_close_matches(w, options, n=3, cutoff=0.6)` | the most similar ones |
| `unified_diff(old, new, lineterm="")` | the difference in `git diff` format |

## unicodedata

| Function | What it does |
|---|---|
| `normalize("NFC", t)` | the composed form (before comparing) |
| `normalize("NFD", t)` | the decomposed form (before dropping accents) |
| `category(ch)` | `Mn` accent, `Lu` uppercase, `Nd` digit... |
| `name(ch)` | the character's Unicode name |

## Turkish

- `"İ".lower()` is two characters; `"I".lower()` is `i` (in Turkish `ı`).
- Convert `I`/`İ` first, then `lower()`; or the other way for `upper()`.
- `sorted` does not know the Turkish alphabet: your own `key` function.
