The card to check while writing paths and moving around with `cd`.

## Signs

| Sign | Meaning | Example |
|---|---|---|
| `/` (at the start) | Start from the root | `/etc/hostname` |
| `/` (in between) | Separates folders | `projects/site/css` |
| `~` | Home folder (`/home/ada`) | `~/notes` |
| `.` | The folder you are in | `./notes` = `notes` |
| `..` | The folder above | `../api` |

## cd

| Command | Where it goes |
|---|---|
| `cd notes` | To the `notes` folder here |
| `cd projects/site` | Two levels down |
| `cd ..` | One level up |
| `cd ../..` | Two levels up |
| `cd ../api` | Up, then into `api` next to it |
| `cd /etc` | Absolute path: `/etc` from anywhere |
| `cd`, `cd ~` | Home folder |
| `cd ~/notes` | `notes` in your home folder, from anywhere |
| `cd -` | The previous folder (prints where it arrived) |
| `cd "my notes"` | A folder with a space in its name |

## Absolute or relative?

- If it starts with `/` or `~` it is **absolute**: it does not matter where
  you are.
- Otherwise it is **relative**: it starts from the folder you are in. If it
  does not work, `pwd` first.

## Errors

| What you see | Meaning |
|---|---|
| `No such file or directory` | No folder with that name, or you are in the wrong place |
| `Not a directory` | What you gave is a file |
| `too many arguments` | You gave two paths; quote a name with spaces |
