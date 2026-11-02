The most used forms of grep, at a glance.

## Basics

| Form | What it does |
|---|---|
| `grep 'pattern' f` | The lines of f that carry the pattern |
| `grep 'pattern' f1 f2` | Several files; the file name in front of each line |
| <code>command &#124; grep 'pattern'</code> | Filters the command's output |
| `grep -r 'pattern' folder` | In the folder and its subfolders |

## Options

| Option | What it does |
|---|---|
| `-i` | Ignore upper/lower case |
| `-n` | Line number (`3:...`) |
| `-c` | The number of matching lines |
| `-v` | The non-matching lines |
| `-w` | Only whole words |
| `-x` | Only whole lines |
| `-o` | Only the matching part |
| `-l` | Only the file names |
| `-E` | Extended expression |
| `-r` | Go into subfolders |

They can be combined: `-in`, `-ic`, `-rl`, `-vi`.

## Exit code

| Code | Meaning |
|---|---|
| 0 | At least one line was found |
| 1 | None was found |
| 2 | Error (missing file, broken pattern) |

## Common patterns

- How many errors: `grep -ic error app.log`
- Errors and warnings: `grep -E 'ERROR|WARN' app.log`
- Everything but info: `grep -vi info app.log`
- In which files: `grep -rl 'TODO' .`
