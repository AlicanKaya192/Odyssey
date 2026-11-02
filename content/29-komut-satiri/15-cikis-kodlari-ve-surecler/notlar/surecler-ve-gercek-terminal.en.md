The terminal in this course is a simulator: it imitates files and commands
inside itself and does not run real programs. Here are the things you will meet
when you move to a real terminal, which cannot be tried here.

## Managing processes

- `ps aux | grep python`: finds the running Python processes and their PIDs.
- `kill 4321`: tells process 4321 to "close". If it does not, `kill -9 4321`
  forces it (unsaved work is lost).
- Ctrl+C stops the command running in front. If a command seems "stuck", this
  is the first thing to try.
- `python train.py &` sends a long job to the background; `jobs` lists it, `fg`
  brings it to the front. If it should keep running after the terminal
  closes, use `nohup` or `tmux`.

## Package managers

| System | Command |
|---|---|
| Ubuntu, Debian | `sudo apt update`, `sudo apt install name` |
| Fedora | `sudo dnf install name` |
| macOS | `brew install name` |
| Windows | `winget install name` |

A package manager installs a program together with its dependencies and puts
it in PATH. Python packages are installed separately with `pip` (covered in the
Python path).

## Finding help

- `man command`: the command's manual. Move with the arrow keys, `/word`
  searches, `q` quits.
- `command --help`: a short summary; most programs have it.
- Searching for an error message exactly as it is is often the fastest way.

## Remote servers

`ssh user@address` opens a command line on another computer (a cloud server, a
school machine). Once connected, everything in this path works the same there:
`ls`, `cd`, `grep`, permissions, scripts. Machine learning models are often
trained like this, on servers with no screen.

## Real Linux on Windows

- **Git Bash**: comes with Git; most commands in this path work, but the
  permissions and processes are Windows'.
- **WSL**: runs a real Linux (like Ubuntu) inside Windows. The closest way to
  work as you would on a Linux server.
