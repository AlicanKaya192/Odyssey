The difference between a working script and a reliable one is a few habits.

## Try it in the terminal first

A script is a record of commands you have seen working in the terminal. Run
each command on its own first, then put it in the file.

## Check the arguments

At the start of the script, check that the arguments you expect have arrived;
if not, say what should be typed and leave with `exit 1`:

```bash
if [ $# -lt 1 ]; then
  echo "usage: backup.sh FILE..."
  exit 1
fi
```

## Always quote variables

`cp $f $f.bak` splits into four separate words for a file named
`my notes.txt`. `cp "$f" "$f.bak"` always works.

## Stop on errors

bash moves on to the next command even when one fails. Real scripts usually
start with this line:

```bash
set -euo pipefail
```

`-e` stops the script when a command fails, `-u` treats an undefined variable
as an error, `-o pipefail` also catches a failure inside a pipe. This terminal
has no `set`; use it in your real scripts.

## Name and explain

- Let the file name say what it does: `backup.sh`, not `x.sh`.
- In one of the first lines, write what the script does and how it is called.
- Give your own variables lower-case names; the capitalised ones belong to the
  environment.

## When not to use a script

A script is great for joining a few commands. If you need calculations, data
structures or hundreds of lines, Python is more readable and has fewer traps.
