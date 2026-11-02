This path covered the everyday use of the command line. If you want to go
further, here are the topics to look at.

## First step: a real terminal

- On Windows, open Git Bash or install Ubuntu with WSL; on macOS and Linux the
  Terminal is already there.
- Repeat the exercises of this path there, with your own files.
- For a week, do your file work (moving, searching, counting) in the terminal
  on purpose.

## Further tools

| Tool | What it is for |
|---|---|
| `awk` | Calculations on columned text: `awk '{s += $3} END {print s}'` |
| `sed` | Find and replace in text: `sed 's/old/new/g'` |
| `xargs` | A command for each item of a list: <code>find . -name '*.tmp' &#124; xargs rm</code> |
| `case` | A decision with many options in a script |
| `read` | Taking input from the user in a script |
| `tee` | Output to both the screen and a file |
| `tmux` | Several windows in one terminal; work goes on if the connection drops |
| `ssh`, `scp` | Working on a remote server, sending files |
| `cron` | Running a command automatically at set times |
| `set -euo pipefail` | Making scripts stop on errors |

## Where to go from here in Odyssey

- **Version Control with Git**: the most used tool on the command line.
- **Docker**: commands, the `RUN` lines in a Dockerfile and a container's
  shell are built on this path.
- **System Design (CI/CD)**: GitHub Actions steps are shell commands; exit
  codes decide pass or fail.
- **Big Data** and **MLOps**: long jobs run on servers, started from the
  terminal.

## Resources

- `man command`: the full manual of every command, always at hand.
- **The Linux Command Line** (William Shotts): a book from start to finish
  that can be read for free.
- **ShellCheck**: a tool that catches quoting and test mistakes in scripts;
  also installed as an editor extension.
