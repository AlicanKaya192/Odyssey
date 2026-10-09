# Text Tools

You saw the string methods (`upper`, `split`, `replace`, `strip`...) in the
Python path. The standard library has a few more text modules, each of which
turns a particular job into one line: the list of punctuation characters
(`string`), wrapping long text into lines (`textwrap`), finding how similar
two texts are and how they differ (`difflib`), accented letters and Unicode
(`unicodedata`). At the end of the section there is a special trap with
Turkish letters.

## string: ready-made character lists

```python
import string

print(string.ascii_lowercase)
print(string.digits, string.punctuation)
text = "Hello, world! 2026."
print("".join(ch for ch in text if ch not in string.punctuation))
print(text.translate(str.maketrans("", "", string.punctuation)))
```

```text
abcdefghijklmnopqrstuvwxyz
0123456789 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
Hello world 2026
Hello world 2026
```

- `string.ascii_lowercase`, `ascii_uppercase`, `digits`, `punctuation`:
  lists that are long and error-prone to type by hand.
- Two ways to delete punctuation: filter one by one with a comprehension, or
  **`str.translate`**. `str.maketrans("", "", to_delete)` builds a
  translation table; `translate` converts the text in one pass and is faster
  on long texts.

## textwrap: wrapping into lines

```python
import textwrap

text = ("Python's standard library has a module for almost every "
        "everyday job, from dates to files.")
for line in textwrap.wrap(text, width=30):
    print(line)
print(textwrap.shorten(text, width=40, placeholder="..."))
print(textwrap.indent("first\nsecond", "> "))


def usage():
    return textwrap.dedent("""\
        Usage:
          report.py FILE
    """)


print(usage())
```

```text
Python's standard library has
a module for almost every
everyday job, from dates to
files.
Python's standard library has a...
> first
> second
Usage:
  report.py FILE
```

- **`wrap(text, width)`** wraps the text into lines of at most `width`
  characters **without breaking words** and gives a list of lines; **`fill`**
  gives the same as one text.
- **`shorten`** cuts what does not fit at a word boundary and adds a mark:
  for preview text in lists.
- **`indent`** puts a prefix at the start of every line (a quote, a code
  block).
- **`dedent`** removes the common leading whitespace: multi-line text written
  indented inside a function starts at the left on screen. The backslash
  after `"""\` swallows the first line break.

## difflib: similarity and differences

```python
import difflib

print(round(difflib.SequenceMatcher(None, "kitten", "sitting").ratio(), 3))
commands = ["start", "stop", "status", "restart", "help"]
print(difflib.get_close_matches("stat", commands))
print(difflib.get_close_matches("hlep", commands, n=1))
old = ["a = 1", "b = 2", "print(a + b)"]
new = ["a = 1", "b = 3", "print(a + b)", "print('done')"]
for line in difflib.unified_diff(old, new, lineterm=""):
    print(line)
```

```text
0.615
['start', 'status', 'restart']
['help']
--- 
+++ 
@@ -1,3 +1,4 @@
 a = 1
-b = 2
+b = 3
 print(a + b)
+print('done')
```

- **`SequenceMatcher(...).ratio()`** is the similarity of two texts, between
  0 and 1.
- **`get_close_matches(word, options)`** gives the most similar options (by
  default at most 3, with similarity at least 0.6). A "did you mean?"
  suggestion for a mistyped command is exactly this: `hlep` → `help`.
- **`unified_diff`** gives the difference of two lists of lines in the format
  of `git diff`: `-` removed, `+` added, a line starting with a space
  unchanged.

## unicodedata: accents and Unicode

```python
import unicodedata

word = "İstanbul"
print(word.lower(), len(word), len(word.lower()))
print(word.lower() == "istanbul", "ISPARTA".lower())


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


print(strip_accents("Café Ünlü Şeker"), strip_accents("ılık"))
a = "é"
b = "e" + chr(0x301)
print(a == b, len(a), len(b))
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))
```

```text
i̇stanbul 8 9
False isparta
Cafe Unlu Seker ılık
False 1 2
True
```

- **The Turkish trap:** Python knows no language when converting case.
  `"İstanbul".lower()` became `i` + a **combining dot** (two characters): on
  screen `i̇stanbul`, length 9, not equal to `"istanbul"`. `"ISPARTA".lower()`
  gave `isparta`, while in Turkish the right one is `ısparta`. When searching
  and comparing Turkish text, you do this conversion yourself (second note).
- **NFD** (decomposition) splits `é` into two characters: `e` + "an accent on
  top"; the category of accent marks is **`Mn`**. Dropping them turns `Café`
  → `Cafe`, `Ünlü` → `Unlu`, `Şeker` → `Seker`. But **`ı` is not an accented
  `i`**, it is a separate letter: it stayed as it was.
- Two texts that look the same may be written differently: the
  one-character `é` and `e` + a combining accent. Before comparing, bring both
  to the same form with **`NFC`**; this happens often with text from files
  and the web.

## string.Template: a simple template

```python
from string import Template

t = Template("Dear $name, your order $order is ready.")
print(t.substitute(name="Ada", order=42))
print(t.safe_substitute(name="Ada"))
try:
    t.substitute(name="Ada")
except KeyError as error:
    print("KeyError:", error)
```

```text
Dear Ada, your order 42 is ready.
Dear Ada, your order $order is ready.
KeyError: 'order'
```

`$name` placeholders are filled with `substitute`; a missing value raises
`KeyError`, while **`safe_substitute`** leaves the missing ones as they are.
An f-string is written inside the code; `Template` is the safe choice when
the text comes **from a user or a file**: no code can be written into it.

## Summary

- `string.punctuation`, `digits`...; `str.translate` to delete.
- `textwrap.wrap`, `fill`, `shorten`, `indent`, `dedent`.
- `difflib.SequenceMatcher(...).ratio()`, `get_close_matches`,
  `unified_diff`.
- `unicodedata.normalize("NFD"/"NFC", ...)`; the accent category is `Mn`.
- Do not trust `lower()` for the Turkish `I`/`İ`.
- `string.Template` for templates from outside.
