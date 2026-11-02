# Exit Codes, Processes and Beyond

Every command, when it ends, leaves something invisible next to what it
printed: a number saying whether it succeeded. Scripts, chains built with `&&`
and automatic systems like GitHub Actions make their decisions by looking at
this number. In the second half of the section we look at things this
terminal cannot imitate but you will use every day in a real terminal:
processes, package managers, help pages and remote servers.

## The exit code: `$?`

```text
~ $ ls docs
a.md  b.md
~ $ echo $?
0
~ $ grep zzz names.txt
~ $ echo $?
1
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ echo $?
2
~ $ ./names.txt
bash: ./names.txt: Permission denied
~ $ echo $?
126
~ $ nosuchcmd
bash: nosuchcmd: command not found
~ $ echo $?
127
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>0</span><span><b>Success.</b> The only "good" code.</span></div>
    <div class="anat-row"><span>1</span><span>A general error; "not found" for grep.</span></div>
    <div class="anat-row"><span>2</span><span>Wrong use: a missing file (ls, grep), an invalid option.</span></div>
    <div class="anat-row"><span>126</span><span>The command was found but could not run (no x permission).</span></div>
    <div class="anat-row"><span>127</span><span>The command was not found.</span></div>
    <div class="anat-row"><span>130</span><span>Stopped with Ctrl+C.</span></div>
  </div>
  <figcaption>Every command leaves a number from 0 to 255 when it ends. Each program decides which error comes with which number; anything other than 0 means "something is wrong".</figcaption>
</figure>

`$?` holds the exit code of the last command. Each program decides which error
comes with which number; the only shared rule is **0 = success**. For grep
"not found" is 1, for ls "no such file" is 2. If a command is not found the
shell gives 127; if it is found but cannot run, 126.

## `$?` belongs only to the last command

```text
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ echo $?
2
~ $ echo $?
0
~ $ grep zzz names.txt | wc -l
0
~ $ echo $?
0
```

- The second `echo $?` gave 0: it now shows the first `echo`'s code. If you
  need the code, read it right away or keep it in a variable: `code=$?`.
- A pipeline's exit code is that of the **last** command. grep found nothing,
  but because `wc` succeeded the chain gave 0. (In real scripts
  `set -o pipefail` changes that.)

## Chaining by the code: `&&`, `||`, `;`

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>a ; b</span><span>First a, then b <b>in every case</b>.</span></div>
    <div class="anat-row"><span>a &amp;&amp; b</span><span>b runs only if a <b>succeeded</b> (0).</span></div>
    <div class="anat-row"><span>a &#124;&#124; b</span><span>b runs only if a <b>failed</b>.</span></div>
    <div class="anat-row"><span>! a</span><span>Turns a's result around.</span></div>
  </div>
  <figcaption>The shortest way to say "if this happened, do that". In a script <code>if</code> does the same job.</figcaption>
</figure>

```text
~ $ mkdir reports && echo created
created
~ $ mkdir reports && echo created
mkdir: cannot create directory 'reports': File exists
~ $ mkdir reports || echo already there
mkdir: cannot create directory 'reports': File exists
already there
~ $ ls nope; echo still runs
ls: cannot access 'nope': No such file or directory
still runs
~ $ grep -q ada names.txt && echo found
found
~ $ grep -q ERROR app.log || echo no errors
no errors
```

- `&&`: go on if the previous one succeeded. The folder could not be created a
  second time, so `created` was not printed.
- `||`: do this if the previous one failed; it means "otherwise".
- `;` is only an order; it does not look at the result.
- `grep -q` prints nothing; it answers only with the code. It is one of the
  commands most used with `&&` and `||`.

`!` turns a command's result around: `! grep -q ERROR app.log && echo ok`
means "if there is no ERROR, print ok".

## if looks at the code too

```text
~ $ if grep -q WARN app.log; then echo warnings; else echo clean; fi
warnings
~ $ if [ -d docs ]; then echo folder; fi
folder
```

`if` actually looks at a command's exit code. `[ -d docs ]` is a command too,
so the `if [ ... ]` form from the Writing Scripts section was a special case of
the same rule. You can write a command like `grep -q` directly as the
condition.

## A script's own code: exit

```text
~ $ cat check_file.sh
#!/bin/bash
if [ ! -f "$1" ]; then
  echo "missing: $1"
  exit 3
fi
echo "found: $1"
~ $ bash check_file.sh names.txt
found: names.txt
~ $ echo $?
0
~ $ bash check_file.sh nope.txt
missing: nope.txt
~ $ echo $?
3
~ $ bash check_file.sh nope.txt || echo the check failed
missing: nope.txt
the check failed
```

Because the script ended with `exit 3`, `$?` became 3 on the caller's side and
`||` kicked in. Without `exit`, a script's code is the code of the last command
it ran. In your own scripts, `exit 0` on success and a separate number for each
kind of error make the caller's job easier. CI systems (GitHub Actions) decide
whether a step passed with exactly this number.

## Processes

This terminal does not run real programs; it imitates everything inside
itself, so the following are not available here. In a real terminal you will
use them often:

| Command | What it does |
|---|---|
| `ps` / `ps aux` | Lists the running processes (each has a PID number) |
| `top` / `htop` | Watches processes live: processor and memory use |
| Ctrl+C | Stops the command in front (exit code 130) |
| `kill PID` | Sends a process a request to stop; `kill -9 PID` forces it |
| `command &` | Starts the command in the background; the prompt returns at once |
| `jobs`, `fg`, `bg` | Lists background jobs, brings them to the front or back |
| Ctrl+Z | Does not stop the command in front, it suspends it (`fg` resumes) |

A **process** is a program that is running. When you close the terminal, the
processes started from it usually close too.

## Beyond: in a real terminal

| Topic | Example | What it is for |
|---|---|---|
| Help | `man ls`, `ls --help` | Every option of a command |
| Package manager | `sudo apt install tree`, `brew install tree` | Installing programs |
| Remote server | `ssh ada@server` | A command line on another computer |
| Sending files | `scp file ada@server:` | Copying to a server |
| Downloading | `curl -O address` | A file from the internet |
| Paged reading | `less file` | Moving around a long file (`q` quits) |

On Windows, WSL (Windows Subsystem for Linux) can be installed for a real Linux
terminal; Git Bash also runs most of the commands in this path.

## Summary

- `$?` is the last command's code; 0 is success, anything else a problem.
- `a && b` if it succeeded, `a || b` if it failed, `a ; b` in every case.
- A pipeline's code is that of its last command.
- `if` looks at a command's code; `grep -q` and `[ ]` are two examples.
- A script chooses its own code with `exit N`.
- Processes: `ps`, `kill`, Ctrl+C, `&`; help: `man`.
