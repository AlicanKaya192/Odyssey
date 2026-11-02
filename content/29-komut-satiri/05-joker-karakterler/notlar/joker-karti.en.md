Patterns and what they match, at a glance.

| Pattern | Matches | Does not match |
|---|---|---|
| `*.txt` | `a.txt`, `notes.txt` | `a.txt.bak`, `.hidden.txt` |
| `photo*` | `photo1.jpg`, `photo` | `my-photo.jpg` |
| `*report*` | `report.txt`, `old-report.md` | `rep.txt` |
| `photo?.jpg` | `photo1.jpg`, `photoA.jpg` | `photo10.jpg` |
| `photo??.jpg` | `photo10.jpg` | `photo1.jpg` |
| `[ab]*` | `a.txt`, `b.csv` | `c.txt` |
| `log[0-9].txt` | `log1.txt` | `log10.txt` |
| `.h*` | `.hidden.txt` | `hidden.txt` |
| `*/` | All (non-hidden) folders | Files |
| `logs/*.log` | The `.log` files in `logs` | Those in subfolders |

## Braces (always expanded)

| What you type | What the shell produces |
|---|---|
| `file{1,2,3}.txt` | `file1.txt file2.txt file3.txt` |
| `{a..d}` | `a b c d` |
| `site/{css,js}` | `site/css site/js` |
| `report.{txt,bak}` | `report.txt report.bak` |

## Turning them off

| What you type | Result |
|---|---|
| `"*.txt"` | A literal `*.txt` |
| `'*.txt'` | A literal `*.txt` |
| `\*.txt` | A literal `*.txt` |

## Remember

- The shell expands wildcards; if nothing matches, the pattern stays as it is.
- See the result first: `echo pattern`.
