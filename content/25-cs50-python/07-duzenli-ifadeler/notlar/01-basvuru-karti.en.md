Everything from Week 7 on one page. Patterns are always raw strings:
`r"..."`.

## Functions

With `import re`:

| Syntax | What it does |
|---|---|
| `re.search(pattern, string)` | searches anywhere in the string; a match or `None` |
| `re.match(pattern, string)` | matches only from the start of the string |
| `re.fullmatch(pattern, string)` | the whole string must fit the pattern |
| `re.sub(pattern, repl, string)` | replaces what it finds; unchanged if nothing matches |
| `re.findall(pattern, string)` | a list of every match (of the groups, if any) |
| `re.split(pattern, string)` | splits by the pattern |

The third argument is flags: `re.IGNORECASE` (case does not matter),
`re.MULTILINE`, `re.DOTALL`.

## Repetition

| Symbol | Meaning |
|---|---|
| `*` | zero or more |
| `+` | one or more |
| `?` | zero or one (optional) |
| `{m}` | exactly `m` |
| `{m,n}` | between `m` and `n` |

Each applies to **the single thing on its left**: `ab+` matches `abbb`, not
`abab`; `(ab)+` matches both.

## Characters and sets

| Symbol | Meaning |
|---|---|
| `.` | any character except a newline |
| `\.` | a literal period (escaped) |
| `[abc]` | `a`, `b` or `c` |
| `[a-z]` | a range |
| `[^@]` | any character except `@` |
| `\d` / `\D` | a digit / not a digit |
| `\s` / `\S` | whitespace / not whitespace |
| `\w` / `\W` | letter, digit, `_` / anything else |
| `\b` | a word boundary (not a character, a position) |

## Position and groups

| Syntax | Meaning |
|---|---|
| `^` | the start of the string (outside square brackets) |
| `$` | the end of the string |
| <code>A&#124;B</code> | A or B |
| `(...)` | a group; captures what is inside |
| `(?:...)` | a group that does not capture |

## The match object

| Syntax | What it gives |
|---|---|
| `matches.group(0)` | the whole match |
| `matches.group(1)` | the first group (groups are counted from 1) |
| `matches.groups()` | all groups, as a tuple |
| `if matches := re.search(...):` | assign and ask (the walrus operator) |

## The lesson's patterns

| Pattern | Job |
|---|---|
| `r"^\w+@(\w+\.)?\w+\.edu$"` | an `.edu` email address, optional subdomain |
| `r"^(.+), *(.+)$"` | `Last, First` → two groups |
| `r"^(https?://)?(www\.)?twitter\.com/"` | the start of the address (to drop with `re.sub`) |
| `r"(?:www\.)?twitter\.com/([a-z0-9_]+)"` | capturing the username |

In a real program, validate an email address with a popular library
(`validators`), not your own pattern.
