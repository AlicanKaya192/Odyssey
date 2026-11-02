# Variables and the Environment

The shell does not only run commands, it also keeps values. You can put a value
into a **variable** and use it again and again, capture a command's output,
and give settings to the programs you run. Most of the settings that change how
programs like Python, git and Docker behave are **environment variables** too.
This section is the foundation of the next one, writing scripts.

## Defining and using a variable

<figure class="fig">
  <pre><code class="language-text">name=Ada          echo "Hello, &#36;name"</code></pre>
  <div class="anat">
    <div class="anat-row"><span>name</span><span>The variable's name: letters, digits, <code>_</code>; it does not start with a digit.</span></div>
    <div class="anat-row"><span>=</span><span>Assignment. <b>No spaces</b> on either side.</span></div>
    <div class="anat-row"><span>Ada</span><span>The value: always text. With spaces, quotes: <code>name="Ada Lovelace"</code>.</span></div>
    <div class="anat-row"><span>&#36;name</span><span>When you use it, a <code>&#36;</code> in front; the shell puts the value in its place.</span></div>
  </div>
  <figcaption>No <code>&#36;</code> when assigning, a <code>&#36;</code> when using. Inside double quotes the value is put in; inside single quotes it is not.</figcaption>
</figure>

```text
~ $ name=Ada
~ $ echo $name
Ada
~ $ echo "Hello, $name"
Hello, Ada
~ $ echo 'Hello, $name'
Hello, $name
~ $ name=Grace
~ $ echo "Hello, $name"
Hello, Grace
~ $ name = Ada
bash: name: command not found
```

- No `$` when assigning: `name=Ada`. A `$` when using it: `$name`.
- A variable can be assigned again; the last value counts.
- **No spaces on either side of the equals sign.** With `name = Ada` the shell
  took `name` for a command.
- Inside double quotes the value is put in, inside single quotes it is not.
  Single quotes leave everything as it is: wildcards and `$` alike. Double
  quotes switch wildcards off but leave `$` on.

## Where the name ends: braces

```text
~ $ file=report
~ $ echo "$file_2026.txt"
.txt
~ $ echo "${file}_2026.txt"
report_2026.txt
~ $ echo "[$nothing]"
[]
~ $ echo "${nothing:-none}"
none
```

The shell reads a variable's name until the letters, digits and `_` end: with
`$file_2026` it looked for a variable named `file_2026`. There is no such
variable, and **an undefined variable gives no error, it becomes empty text**;
`.txt` was left over. You mark the end of the name with `${file}`.

`${nothing:-none}` means "if empty, use this value"; a short way to give a
default value in scripts.

## Use a variable in quotes

```text
~ $ greeting="Hello   world"
~ $ echo $greeting
Hello world
~ $ echo "$greeting"
Hello   world
```

Without quotes the shell split the value of `$greeting` at the spaces and gave
`echo` two separate words; the extra spaces in between were lost. Double quotes
keep the value in one piece. Use every variable that may contain spaces
(especially file names) as `"$name"`.

## Capturing a command's output

```text
~ $ count=$(ls docs | wc -l)
~ $ echo "docs has $count files"
docs has 5 files
~ $ echo $((count * 2))
10
~ $ lines=$(wc -l < names.txt)
~ $ echo "names.txt has $lines lines"
names.txt has 7 lines
```

- `$( command )` runs the command and puts its output in its place (*command
  substitution*). The result can be assigned to a variable or used directly
  inside a piece of text.
- `$(( ... ))` does integer arithmetic; inside it you do not need a `$` in
  front of a variable.

## The shell's ready-made variables

```text
~ $ echo $HOME
/home/ada
~ $ echo $USER
ada
~ $ echo $PWD
/home/ada
~ $ cd docs
~/docs $ echo $PWD
/home/ada/docs
~/docs $ cd
~ $ echo $SHELL
/bin/bash
```

The shell fills in some variables itself when it starts. `HOME` is your home
folder (the `~` shortcut uses it), `USER` your user name, `PWD` the current
folder (it changes with `cd`), `SHELL` the shell you use. These are written in
**capitals**; giving your own variables lower-case names avoids mix-ups.

## Environment variables: export

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Shell variable</h4><p><code>city=London</code></p><p>Only in this shell</p><p>Programs it starts do not see it</p></div>
    <div class="ok"><h4>Environment variable</h4><p><code>export city=London</code></p><p>In this shell and every program it starts</p><p>Shows up in the <code>env</code> list</p></div>
  </div>
  <figcaption>A program (Python, git, a script) reads its settings from environment variables. To give it a value, <code>export</code>.</figcaption>
</figure>

```text
~ $ city=London
~ $ bash -c 'echo "[$city]"'
[]
~ $ export city
~ $ bash -c 'echo "[$city]"'
[London]
~ $ printenv city
London
~ $ unset city
~ $ printenv city
```

`bash -c '...'` starts a new shell and runs the command in the quotes; here it
stands in for "another program". On the first try the new shell did not see
`city`: a plain variable lives only in the shell where it was defined. `export`
moved the variable into the **environment**; every program the shell starts
from now on sees it. `printenv` prints an environment variable, `unset`
removes a variable.

You can also give a value to **a single command** only:

```text
~ $ GREETING=Hi bash -c 'echo $GREETING'
Hi
~ $ echo "[$GREETING]"
[]
```

An assignment written in front of a command counts only for that command; it
left no trace in the shell.

## The whole environment: env

```text
~ $ env
HOME=/home/ada
USER=ada
LOGNAME=ada
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
PWD=/home/ada
LANG=en_US.UTF-8
TERM=xterm-256color
~ $ env | grep HOME
HOME=/home/ada
```

`env` prints the list of environment variables. On a real computer the list
is much longer; you filter what you are looking for with `grep`.

## PATH: where commands are looked for

When you type a command, the shell looks for it in the folders in the `PATH`
variable, from left to right. The folders are separated by `:`.

```text
~ $ echo $PATH
/usr/local/bin:/usr/bin:/bin
~ $ which ls
/usr/bin/ls
~ $ ls -l tools/greet
-rwxr-xr-x 1 ada ada 34 Oct  7 10:00 tools/greet*
~ $ greet
bash: greet: command not found
~ $ export PATH="$HOME/tools:$PATH"
~ $ echo $PATH
/home/ada/tools:/usr/local/bin:/usr/bin:/bin
~ $ greet
Hello from greet
~ $ which greet
/home/ada/tools/greet
```

- `which ls` tells you where the command was found in PATH.
- `greet` was not found even though `tools/greet` is executable: `tools` is not
  in PATH.
- `export PATH="$HOME/tools:$PATH"` added the new folder to the front and
  **kept the old value**. Had you forgotten to write `$PATH` at the end, PATH
  would be only `tools` and not even `ls` could be found.

When a program says `command not found` even though you installed it, this is
usually the reason: the folder it was installed in is not in PATH.

## Making it permanent: ~/.bashrc

The variables, `export`s and aliases you define are lost when the terminal
closes. bash reads the `.bashrc` file in the home folder in every new
terminal; the lines you want to keep are written there:

```text
~ $ cat .bashrc
# ~/.bashrc: bash reads this file when a new terminal opens.
# Aliases and settings written here last for every session.
~ $ echo "alias ll='ls -l'" >> .bashrc
~ $ ll names.txt
bash: ll: command not found
~ $ source .bashrc
~ $ ll names.txt
-rw-r--r-- 1 ada ada 47 Oct  7 10:00 names.txt
~ $ type ll
ll is aliased to `ls -l'
```

- With `>>` the line was added to the **end** of the file; with `>` the old
  content would have been erased.
- Right after adding it, `ll` did not work: the file is only read when a
  **new** terminal opens. `source .bashrc` made the current shell read it.
- `type ll` tells you what a name is: an alias, one of the shell's own
  commands, or a program.

A PATH addition is usually written in `.bashrc` too:
`export PATH="$HOME/tools:$PATH"`.

## Summary

| Form | What it does |
|---|---|
| `name=value` | Defines a variable (no spaces) |
| `"$name"`, `"${name}"` | Uses the value |
| `${name:-default}` | A default when empty |
| `$(command)` | The command's output |
| `$((a + b))` | Arithmetic |
| `export NAME=value` | An environment variable |
| `NAME=value command` | Only for that command |
| `env`, `printenv NAME` | Shows the environment |
| `unset name` | Removes a variable |
| `export PATH="$HOME/x:$PATH"` | Adds a folder to PATH |
| `source ~/.bashrc` | Reads the settings file again |
