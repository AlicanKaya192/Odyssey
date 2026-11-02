Every redirection, at a glance.

## Streams

| Number | Name | By default |
|---|---|---|
| 0 | stdin (standard input) | Keyboard |
| 1 | stdout (standard output) | Screen |
| 2 | stderr (standard error) | Screen |

## Spellings

| Spelling | What it does |
|---|---|
| `command > f` | Writes stdout to f (f is written from the start) |
| `command >> f` | Adds stdout to the end of f |
| `command 2> f` | Writes stderr to f |
| `command 2>> f` | Adds stderr to the end of f |
| `command > f 2>&1` | Both into f |
| `command &> f` | The same, short spelling (bash) |
| `command > out.txt 2> err.txt` | Output and errors into separate files |
| `command > /dev/null` | Throw the output away |
| `command 2> /dev/null` | Throw the errors away |
| `command < f` | Read the input from f |
| `command < in.txt > out.txt` | Read from a file, write to a file |
| `> f` | Empty f (or create it empty) |

## Remember

- Spaces are free: `> f` and `>f` are the same. But `2>` stays together: if
  you write `2 > f`, the `2` becomes an argument of the command.
- `2>&1` goes **after** the other redirection: `> f 2>&1`.
- Never write with `>` into the file you are reading in the same command.
