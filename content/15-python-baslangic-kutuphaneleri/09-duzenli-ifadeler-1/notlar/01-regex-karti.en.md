## Functions

| Code | Returns |
|---|---|
| `re.search(p, text)` | the first match (anywhere) or `None` |
| `re.match(p, text)` | a match at the start or `None` |
| `re.fullmatch(p, text)` | a match if the whole text fits, else `None` |
| `re.findall(p, text)` | a list of all matches |
| `m.group()`, `m.start()`, `m.end()` | the found text, its start, its end |

## Characters

| Code | Meaning |
|---|---|
| `\d` / `\D` | a digit / not a digit |
| `\w` / `\W` | a word character / not one |
| `\s` / `\S` | whitespace / not whitespace |
| `.` | any character except a line break |
| `[abc]`, `[a-z0-9]` | one of those listed |
| `[^abc]` | one not listed |
| `\.`, `\(`, `\?` | the special character itself |

## Quantity and position

| Code | Meaning |
|---|---|
| `?` | 0 or 1 |
| `*` | 0 or more |
| `+` | 1 or more |
| `{n}`, `{n,}`, `{n,m}` | exactly n, at least n, between n and m |
| `^`, `$` | the start, the end of the text |
| `\b` | a word boundary |

## Common patterns

| Pattern | What it finds |
|---|---|
| `\d+` | integers |
| `-?\d+` | signed integers |
| `\d+\.\d+` | decimal numbers |
| `\d{4}-\d{2}-\d{2}` | the ISO date format |
| `#\w+` | hashtags |
| `\bword\b` | only the whole word |

## Rules

- Patterns are always `r"..."`.
- Use `fullmatch` to validate; `search` also finds a fitting part of the text.
- `re.escape` text from a user before putting it in a pattern.
- `flags=re.IGNORECASE`: case does not matter.
