The commands of this section, at a glance.

| Command | What it does |
|---|---|
| `cat file` | The whole file |
| `cat -n file` | With line numbers |
| `head file` | The first 10 lines |
| `head -n 5 file` / `head -5 file` | The first 5 lines |
| `tail file` | The last 10 lines |
| `tail -n 5 file` / `tail -5 file` | The last 5 lines |
| `tail -n +5 file` | From line 5 to the end |
| `tail -f file` | Follows the end, prints new lines (in a real terminal) |
| `wc file` | Lines, words, bytes |
| `wc -l file` | Line count |
| `wc -w file` | Word count |
| `wc -c file` | Byte count |

## Which one when?

| Question | Command |
|---|---|
| How does the file start? (header line, columns) | `head -n 3` |
| What just happened? (log file) | `tail` |
| How many records / lines? | `wc -l` |
| What is on line 40? | `cat -n`, or `head -n 40` and look at its last line |
| Reading a long document comfortably | `less` (in a real terminal) |

## Common mistakes

| What you see | Why |
|---|---|
| `head: invalid number of lines: 'ten'` | The number is written in digits |
| `tail: cannot open 'x' for reading: No such file or directory` | No such file, or you are in the wrong place |
| `wc: logs: Is a directory` | A folder itself is not counted; give a file inside it |
