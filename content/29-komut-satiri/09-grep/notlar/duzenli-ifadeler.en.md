grep's pattern is a regular expression. Here are the parts you need most
often; the whole subject is a language of its own.

## Special characters

| Form | Meaning | Example | Matches |
|---|---|---|---|
| `^` | Start of the line | `'^a'` | ada, alan |
| `$` | End of the line | `'e$'` | grace, katherine |
| `.` | Any single character | `'d.sk'` | disk, desk |
| `[abc]` | One of the characters in the brackets | `'[0-9]'` | any digit |
| `[^abc]` | One character other than these | `'[^0-9]'` | not a digit |
| `x*` | Zero or more of x | `'ab*c'` | ac, abc, abbc |
| `.*` | Any text | `'user.*in'` | user ada logged in |

With `-E` also:

| Form | Meaning | Example |
|---|---|---|
| `x+` | One or more of x | `'[0-9]+%'` |
| `x?` | x may or may not be there | `'colou?r'` |
| <code>A&#124;B</code> | A or B | <code>'ERROR&#124;WARN'</code> |
| `( )` | Grouping | `'(ab)+'` |

## Searching for a special character itself

To search for a real dot or star, put a backslash in front of it: `'1\.5'`,
`'a\*b'`. Or, if you want no regular expression at all, `grep -F` (plain text).

## The difference from wildcards

| | Wildcard (shell) | Regular expression (grep) |
|---|---|---|
| Any text | `*` | `.*` |
| One character | `?` | `.` |
| Applies to | File names | The inside of lines |

## Quotes

Always write the pattern in single quotes. If you write `grep a* f` without
quotes, the shell first expands `a*` into file names and grep sees a
completely different pattern.
