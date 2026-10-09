## Groups

| Code | Meaning |
|---|---|
| `(...)` | a capturing group |
| `(?P<name>...)` | a named group |
| `(?:...)` | a non-capturing group (only a boundary) |
| `m.group(1)`, `m.group("name")`, `m["name"]` | one group |
| `m.groups()` | all groups, a tuple |
| `m.groupdict()` | the named groups, a dictionary |

## Pattern pieces

| Code | Meaning |
|---|---|
| <code>a&#124;b</code> | a or b |
| `+?`, `*?`, `??` | lazy (as little as possible) |
| `\1` (inside a pattern) | the same as group 1 again: `(\w)\1` → `ll`, `ss` |

## Functions

| Code | What it does |
|---|---|
| `re.findall(p, t)` | matches without groups, group tuples with groups |
| `re.finditer(p, t)` | match objects, one by one |
| `re.sub(p, new, t)` | replaces; `\1`, `\g<name>` in the new text |
| `re.sub(p, function, t)` | for each match, what the function returns |
| `re.sub(..., count=n)` | only the first n |
| `re.subn(p, new, t)` | `(new text, number replaced)` |
| `re.split(p, t)` | splits by the pattern |
| `re.compile(p, flags)` | a compiled pattern |

## Flags

| Flag | Effect |
|---|---|
| `re.IGNORECASE` (`re.I`) | case does not matter |
| `re.MULTILINE` (`re.M`) | `^ $` are each line's start/end |
| `re.DOTALL` (`re.S`) | `.` also matches a line break |
| `re.VERBOSE` (`re.X`) | spaces and comments allowed in the pattern |

Combining: `re.I | re.M`.
