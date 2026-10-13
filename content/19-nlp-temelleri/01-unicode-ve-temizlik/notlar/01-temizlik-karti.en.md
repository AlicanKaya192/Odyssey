The tools used most often when cleaning text.

## Functions

| Tool | What it does | Example |
|---|---|---|
| `ord(c)` / `chr(n)` | Character ↔ code point | `ord("ş")` → 351 |
| `s.encode("utf-8")` / `b.decode("utf-8")` | Text ↔ bytes | `"ş".encode()` → `b'\xc5\x9f'` |
| `unicodedata.normalize("NFC", s)` | Combines a letter and its mark | the two "café"s become equal |
| `unicodedata.normalize("NFD", s)` | Splits a letter from its mark | the first step of removing accents |
| `unicodedata.normalize("NFKC", s)` | Simplifies visual variants | "ＡＢＣ" → "ABC", "…" → "..." |
| `unicodedata.combining(c)` | Is it a combining mark? | filtering accents |
| `unicodedata.name(c)` | The character's official name | hunting an invisible one |
| `html.unescape(s)` | Decodes HTML entities | `&amp;` → `&` |
| `re.sub(r"<[^>]+>", " ", s)` | Removes HTML tags | `<br>` → a space |
| `str.maketrans` + `translate` | Maps letter by letter | Turkish `lower` |
| `" ".join(s.split())` | Turns every space into one space | tabs, `\xa0`, line ends |
| `ascii(s)` | Writes invisible characters as codes | `'a\xa0b'` |

## Invisible and look-alike characters

| Character | Code | Where it comes from | Problem |
|---|---|---|---|
| No-break space | U+00A0 | Web pages, word processors | `split(" ")` does not split at it |
| Zero-width space | U+200B | Web editors | Invisible, sticks to a word |
| BOM | U+FEFF | Windows Notepad | Breaks the first line of a file |
| Soft hyphen | U+00AD | Copied text | Invisible, splits a word |
| Curly quotes | U+2018, U+2019, U+201C, U+201D | Word processors | Do not match `'` |
| Long dashes | U+2013, U+2014 | Word processors | Do not match `-` |

`str.split()` called without an argument counts the no-break space as a
space, but the zero-width space, the BOM and the soft hyphen are not
"spaces": they have to be removed by hand.

## A suggested order

1. Read with the right encoding (`encoding="utf-8"`, `"utf-8-sig"` if there
   is a BOM).
2. Decode HTML entities, remove tags.
3. Normalise (NFC; NFKC if visual variants should go too).
4. Straighten quotes and dashes, remove invisible characters.
5. Collapse spaces into one.
6. Depending on the task: lowercase (with `translate` for Turkish), accents,
   punctuation.

The first five steps are harmless for almost any task. The sixth can remove
information; decide each time by looking at your task.
