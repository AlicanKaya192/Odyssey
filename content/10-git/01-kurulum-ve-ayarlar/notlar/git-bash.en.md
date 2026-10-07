The terminal that comes with Git on Windows is Git Bash. It is like a Linux
terminal and behaves differently from Windows' own terminals (Command Prompt,
PowerShell) in a few places.

## Paths

Git Bash writes Windows paths in Linux style:

| Windows | Git Bash |
|---|---|
| `C:\Users\Ada` | `/c/Users/Ada` |
| `D:\Projects\site` | `/d/Projects/site` |
| Your home folder | `~` (= `/c/Users/Ada`) |

- The separator is `/`, not `\`.
- The drive letter comes first, in lower case: `/c/`, `/d/`.
- Put paths with spaces in quotes: `cd "/c/Users/Ada/My Projects"`.

## Opening Git Bash in a folder

In File Explorer, right-click the folder → **Open Git Bash here** (on
Windows 11, first **Show more options**). The terminal opens right in that
folder, no `cd` needed.

The other way round, to open the folder you are in from the terminal:

```bash
explorer .     # open in File Explorer
code .         # open in VS Code (if VS Code is installed)
```

`.` means "the folder I am in".

## Copying and pasting

In Git Bash `Ctrl+C` does not copy; it **stops the running command**.
Instead:

- Text you select with the mouse is copied automatically.
- **Shift+Insert** pastes; the right-click menu also has **Paste**.

## Useful keys

| Key | What it does |
|---|---|
| ↑ / ↓ | Previous / next command |
| Tab | Completes a file or folder name |
| Ctrl+C | Stops the running command |
| Ctrl+L | Clears the screen (`clear`) |
| `q` | Leaves the pager in long output such as `git log` |

The last row matters: when `git log` is long, the output opens in a
**pager** and you see `:` or `(END)` on the bottom line. Move with the arrow
keys and space, leave with **`q`**. Most people who think they are stuck are
here.
