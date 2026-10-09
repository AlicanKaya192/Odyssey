# Regular Expressions 1: Searching with Patterns

Finding every phone number in a text, checking that a product code is
written in the right format, pulling dates out of a log file... Doing this
with string methods like `find`, `split` and `isdigit` takes long, fragile
code. A **regular expression** (**regex** for short) is a language for
writing the **pattern** of what you are looking for in one line: "three
digits, a dash, four digits". In Python it is used through the **`re`**
module.

In this section we see the basics of the pattern language; in the next one,
pulling out parts with groups and replacing.

## A first example

```python
import re

text = "Order 66 shipped 3 items for 120 TL on 2026-03-15"
print(re.findall(r"\d+", text))
```

```text
['66', '3', '120', '2026', '03', '15']
```

`\d` means "a digit", `+` means "one or more": `\d+` found every run of
digits next to each other. With string methods the same job would need a
loop, `isdigit` and a few variables.

The **`r`** (raw string) at the start of the pattern matters; the reason is
below.

## Four ways to search

```python
import re

text = "Call 555-1234 or 555-9876"
m = re.search(r"\d{3}-\d{4}", text)
print(m.group(), m.start(), m.end())
print(re.match(r"\d{3}", text), re.match(r"Call", text).group())
print(re.fullmatch(r"\d{3}-\d{4}", "555-1234") is not None)
print(re.fullmatch(r"\d{3}-\d{4}", "555-12345"))
print(re.findall(r"\d{3}-\d{4}", text))
```

```text
555-1234 5 13
None Call
True
None
['555-1234', '555-9876']
```

| Function | What it does | If nothing is found |
|---|---|---|
| `re.search(pattern, text)` | the first match **anywhere** in the text | `None` |
| `re.match(pattern, text)` | only at the **start** of the text | `None` |
| `re.fullmatch(pattern, text)` | the **whole** text must fit the pattern | `None` |
| `re.findall(pattern, text)` | **all** matches, a list | `[]` |

- `search`, `match` and `fullmatch` return a **match object**: `group()` is
  the found text, `start()` / `end()` its position.
- Because the text starts with `Call`, `match(r"\d{3}")` found nothing
  (`None`).
- For **validation** (is a code or number in the right format?) use
  `fullmatch`: `"555-12345"` was rejected because of the extra digit, even
  though its start fits.

## Character classes

Each piece of a pattern describes one **character** or one **kind of
character**.

| Code | Matches |
|---|---|
| `\d` | a digit (0–9) |
| `\w` | a letter, digit or `_` (a word character) |
| `\s` | a space, tab or line break |
| `.` | **any** character except a line break |
| `[abc]` | `a`, `b` or `c` |
| `[A-Z]`, `[0-9]` | a range |
| `[^a-z]` | a character **outside** `a`–`z` |
| `\D`, `\W`, `\S` | uppercase: the opposite (not a digit...) |

```python
import re

text = "id: A7, B12; total = 9.5 kg"
print(re.findall(r"\d", text))
print(re.findall(r"\d+", text))
print(re.findall(r"[A-Z]\d+", text))
print(re.findall(r"\w+", text))
print(re.findall(r"\d+\.\d+", text), re.findall(r"\d.\d", "9.5 9x5"))
print(re.findall(r"[^a-z\s]+", "abc DEF 12 gh!"))
```

```text
['7', '1', '2', '9', '5']
['7', '12', '9', '5']
['A7', 'B12']
['id', 'A7', 'B12', 'total', '9', '5', 'kg']
['9.5'] ['9.5', '9x5']
['DEF', '12', '!']
```

- `\d` found each digit separately; `\d+` the runs.
- `[A-Z]\d+`: an uppercase letter followed by digits.
- `\w+` found the words; `9.5` was split in two because the dot is not a
  word character.
- In a decimal number the dot is written as **`\.`**. A bare `.` means "any
  character", so it also caught `9x5`.
- `[^a-z\s]+`: runs of characters that are **not** lowercase letters or
  spaces.

## How many? Quantifiers and anchors

| Code | Meaning |
|---|---|
| `?` | 0 or 1 (optional) |
| `*` | 0 or more |
| `+` | 1 or more |
| `{3}` | exactly 3 |
| `{2,}` / `{2,4}` | at least 2 / between 2 and 4 |
| `^` / `$` | the start / end of the text |
| `\b` | a word boundary |

```python
import re

words = ["color", "colour", "colouur", "flavor"]
print([w for w in words if re.fullmatch(r"colou?r", w)])
print(re.findall(r"\b\w{5}\b", "the quick brown fox jumps over lazy dogs"))
print(re.findall(r"[aeiou]{2,}", "queue cooperate beautiful"))
lines = ["Error: disk full", "No Error"]
print([bool(re.search(r"^Error", line)) for line in lines])
names = ["data.csv", "data.csv.bak"]
print([bool(re.search(r"\.csv$", name)) for name in names])
print(re.findall(r"python", "Python python PYTHON", flags=re.IGNORECASE))
```

```text
['color', 'colour']
['quick', 'brown', 'jumps']
['ueue', 'oo', 'eau']
[True, False]
[True, False]
['Python', 'python', 'PYTHON']
```

- `colou?r`: the `u` is optional; the one with two `u`s was rejected.
- `\b\w{5}\b`: words of exactly five letters. Without `\b`, the first five
  letters of longer words would match too (`beautiful` → `beaut`).
- `^Error` found only the line with `Error` at the **start**, `\.csv$` only
  the name **ending** in `.csv`.
- **`flags=re.IGNORECASE`** ignores upper and lower case.

## r"..." and special characters

```python
import re

print(len("\b"), len(r"\b"))
print(re.findall("\bcat\b", "cat concat cat"))
print(re.findall(r"\bcat\b", "cat concat cat"))
print(re.findall(r"3.5", "3.5 345 3x5"), re.findall(r"3\.5", "3.5 345 3x5"))
print(re.escape("price (USD)?"))
m = re.search(r"\d+", "no digits here")
print(m)
try:
    print(m.group())
except AttributeError as error:
    print("AttributeError:", error)
```

```text
1 2
[]
['cat', 'cat']
['3.5', '345', '3x5'] ['3.5']
price\ \(USD\)\?
None
AttributeError: 'NoneType' object has no attribute 'group'
```

- In a Python string `\b` is a single character (backspace). `r"\b"` is two
  characters: a backslash and `b`; that is what reaches the regex. Without
  `r`, `\bcat\b` found nothing. **Always write patterns as `r"..."`.**
- `. ? * + ( ) [ ] { } ^ $ | \` have special meanings in a regex; to search
  for them as letters, put a `\` in front. To search for text coming from a
  user, **`re.escape`** escapes them all for you.
- `search` returns `None` when it finds nothing; `None.group()` raises
  **`AttributeError`**. Check first: `if m: ...`.

## Summary

- `re.search` (anywhere), `re.match` (at the start), `re.fullmatch` (the
  whole text; for validation), `re.findall` (all, a list).
- `\d \w \s .`, `[...]`, `[^...]`; uppercase `\D \W \S` are the opposite.
- `? * + {n} {m,n}`; `^ $ \b`; `flags=re.IGNORECASE`.
- Patterns are always `r"..."`; escape special characters with `\` or
  `re.escape`.
- No match gives `None`: check before `.group()`.
