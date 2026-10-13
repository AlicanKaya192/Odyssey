As information extraction rules grow, one-line regular expressions become
unreadable. Three habits make the work easier.

## Named groups and commented layout

```python
import re

AMOUNT = re.compile(r"""
    \$                          # dollar sign
    (?P<whole>\d{1,3}(?:,\d{3})*)  # whole part with thousands separators
    (?:\.(?P<cents>\d{2}))?     # optional cents
""", re.VERBOSE)

for match in AMOUNT.finditer("Paid $1,200.00, refunded $5."):
    parts = match.groupdict()
    value = int(parts["whole"].replace(",", "")) + int(parts["cents"] or 0) / 100
    print(match.group(), parts, value)
```

```text
$1,200.00 {'whole': '1,200', 'cents': '00'} 1200.0
$5 {'whole': '5', 'cents': None} 5.0
```

- `re.VERBOSE` ignores spaces and everything after `#`: you can write the
  rule piece by piece, with comments. (If the expression needs a real space,
  write `\ ` or `\s`.)
- `(?P<name>...)` is a **named group**: you reach a part of the match by
  name instead of by number (`groupdict()`). An optional group that did not
  match is `None`; hence `parts["cents"] or 0`.
- `(?:...)` is a **non-capturing group**: only for grouping. When
  `re.findall` sees a capturing group it returns the group instead of the
  whole match; that is why the amount rule in the lesson used `(?:...)`.

## Greedy and lazy

```python
html = "<b>late</b> and <i>damaged</i>"
print(re.findall(r"<.*>", html))
print(re.findall(r"<.*?>", html))
```

```text
['<b>late</b> and <i>damaged</i>']
['<b>', '</b>', '<i>', '</i>']
```

`.*` is **greedy**: it matches as much as it can and swallows everything from
the first `<` to the last `>`. `.*?` is **lazy**: it matches as little as it
can. When pulling out what is between tags, quotes or brackets you almost
always need the lazy one (or "anything but the closing mark", such as
`<[^>]*>`).

## Test your rules

Keep a few examples next to every rule: ones that should match and ones that
should **not**. The gold standard in the lesson was a small version of this.
Seeing that old examples still work when you widen a rule catches the most
common mistake with regular expressions: breaking one thing while fixing
another.
