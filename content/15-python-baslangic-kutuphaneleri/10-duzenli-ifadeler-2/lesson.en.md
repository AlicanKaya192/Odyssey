# Regular Expressions 2: Groups and Replacing

In the previous section we found **where** a pattern occurs. Often more is
needed: taking a date's year, month and day **separately**, splitting a log
line into its parts, **replacing** something in a text. In this section we
see pulling out parts with groups, replacing with `sub`, splitting with
`split`, and how much a pattern "swallows" (greedy / lazy).

## Groups: taking parts separately

Putting part of a pattern in **parentheses** makes it a **group**; after a
match, each group is read on its own.

```python
import re

m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Due on 2026-03-15, paid")
print(m.group(0), m.group(1), m.group(2), m.group(3))
print(m.groups())
year, month, day = m.groups()
print(int(day) + 1)
```

```text
2026-03-15 2026 03 15
('2026', '03', '15')
16
```

- `group(0)` (or `group()`) is the whole match; `group(1)`, `group(2)`... are
  the parentheses, from left to right.
- `groups()` gives all groups as a tuple; it can be unpacked straight into
  variables.
- Groups are **text** too: `int(...)` for arithmetic.

## Named groups

As the number of groups grows, numbers like `group(3)` become unreadable.
**`(?P<name>...)`** gives a group a name:

```python
import re

pattern = r"(?P<user>[\w.]+)@(?P<domain>[\w.]+)"
m = re.search(pattern, "Write to ada.l@example.com today")
print(m.group("user"), m.group("domain"))
print(m.groupdict())
```

```text
ada.l example.com
{'user': 'ada.l', 'domain': 'example.com'}
```

`groupdict()` turns the named groups into a dictionary. `[\w.]+` means "a
word character or a dot": inside square brackets the dot loses its special
meaning and is searched as a letter.

## findall and finditer with groups

```python
import re

text = "pen=3, book=12, ink=7"
print(re.findall(r"\w+=\d+", text))
print(re.findall(r"(\w+)=(\d+)", text))
print({name: int(n) for name, n in re.findall(r"(\w+)=(\d+)", text)})
for m in re.finditer(r"(\w+)=(\d+)", text):
    print(m.start(), m.group(1))
```

```text
['pen=3', 'book=12', 'ink=7']
[('pen', '3'), ('book', '12'), ('ink', '7')]
{'pen': 3, 'book': 12, 'ink': 7}
0 pen
7 book
16 ink
```

- When the pattern has **no** groups, `findall` gives the matching texts.
- When it **has** groups, it gives the **groups**, not the whole match: a
  tuple per match. That turned the `key=value` text into a dictionary in one
  line.
- **`finditer`** gives the match **object** of each match in turn: when you
  need extra information like the position (`start`), or when the text is
  very long (it does not collect them all in a list).

## Either or: |

```python
import re

print(re.findall(r"cat|dog", "cat, dog, bird, catalog"))
print(re.findall(r"\b(?:cat|dog)s?\b", "cats and dogs and catalog"))
print(re.findall(r"\b(cat|dog)s?\b", "cats and dogs and catalog"))
```

```text
['cat', 'dog', 'cat']
['cats', 'dogs']
['cat', 'dog']
```

- `cat|dog` means "cat **or** dog". Without word boundaries the `cat` in
  `catalog` came too.
- Parentheses are needed to limit the reach of `|`. **`(?:...)`** is a
  non-capturing group: it only draws a boundary and does not change what
  `findall` returns. With plain parentheses, `findall` returned only the
  group (`cat`, `dog`) and the `s` was lost.

## Greedy and lazy

```python
import re

html = "<b>bold</b> and <i>italic</i>"
print(re.findall(r"<.+>", html))
print(re.findall(r"<.+?>", html))
print(re.findall(r"<(\w+)>", html))
```

```text
['<b>bold</b> and <i>italic</i>']
['<b>', '</b>', '<i>', '</i>']
['b', 'i']
```

`+` and `*` are **greedy**: they swallow as much as they can. `<.+>` took
everything from the first `<` to the **last** `>`. With a `?` after them
they become **lazy**: as little as possible. `<.+?>` found each tag
separately. The sturdiest way is often to narrow what you want: `<(\w+)>`
only the opening tags made of letters.

## Replacing and splitting: sub, split

```python
import re

print(re.sub(r"\s+", " ", "too    many   spaces"))
text = "on 15/03/2026 and 01/04/2026"
print(re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", text))
print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "3 apples, 10 pears"))
print(re.split(r"[,;]\s*", "a, b;c; d"))
print(re.sub(r"\d", "#", "card 1234-5678", count=4))
```

```text
too many spaces
on 2026-03-15 and 2026-04-01
6 apples, 20 pears
['a', 'b', 'c', 'd']
card ####-5678
```

- **`re.sub(pattern, new, text)`** replaces every match: runs of spaces
  became one.
- In the new text, **`\1`, `\2`, `\3`** put the groups back: day/month/year
  turned into year-month-day order. The new text is written as `r"..."` too.
- Instead of a new text, a **function** can be given: it is called with each
  match object and the text it returns is put in. Here the numbers were
  doubled.
- **`re.split`** splits by a pattern: a comma or a semicolon, then optional
  spaces. `str.split` can take only one separator.
- `count=4` replaced only the first four matches.

## compile and flags

If the same pattern is used many times, it is compiled once with
**`re.compile`**; the code gets more readable and the pattern gets a name.

```python
import re

log = """2026-03-15 10:02 ERROR disk full
2026-03-15 10:05 INFO saved
2026-03-15 10:09 ERROR timeout"""
line_re = re.compile(r"^(\S+) (\S+) (ERROR|INFO) (.+)$", re.MULTILINE)
for date, time, level, message in line_re.findall(log):
    if level == "ERROR":
        print(time, message)
print(len(re.findall(r"^2026", log)))
print(len(re.findall(r"^2026", log, flags=re.MULTILINE)))
```

```text
10:02 disk full
10:09 timeout
1
3
```

- A compiled pattern has `search`, `findall`, `sub` methods too.
- `^` and `$` are normally the start and end of **the whole text**. With
  **`re.MULTILINE`** they become the start and end of **every line**: in the
  three-line log `^2026` was found three times instead of once.
- Flags are combined with `|`: `re.MULTILINE | re.IGNORECASE`.

## Summary

- `(...)` is a group: `group(n)`, `groups()`; `(?P<name>...)` is a named
  group, `groupdict()`.
- With groups in the pattern, `findall` gives the groups (tuples); `finditer`
  gives match objects.
- `a|b` is either or; `(?:...)` is a non-capturing group.
- `+ *` are greedy, `+? *?` lazy.
- `re.sub` (`\1` in the new text, or a function), `re.split`, `count=`.
- `re.compile`; with `re.MULTILINE`, `^ $` work on every line.
