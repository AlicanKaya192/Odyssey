The most used options of `ls`.

| Option | Name | What it does |
|---|---|---|
| `-l` | long | One line per file: type, permissions, owner, group, size, date, name |
| `-a` | all | Hidden files and `./`, `../` |
| `-A` | almost all | Hidden files, without `./` and `../` |
| `-h` | human-readable | Sizes with `K`, `M`, `G` (together with `-l`) |
| `-1` | one | Each name on its own line |
| `-R` | recursive | Together with subfolders |
| `-d` | directory | The folder itself, not its contents |

## The most used combinations

| Command | When |
|---|---|
| `ls -la` | Looking at everything in a folder, in detail |
| `ls -lh` | Which file is big? |
| `ls -lah` | Both at once |
| `ls -ld folder` | Looking at a folder's permissions |

On many Linux systems the shortcut `ll` is defined as `ls -l` (or `ls -alF`).

## In real ls but not in this terminal

| Option | What it does |
|---|---|
| `-t` | Sorts by time (newest first) |
| `-S` | Sorts by size |
| `-r` | Reverses the order |

`ls -lt` is the quick answer to "what changed last".
