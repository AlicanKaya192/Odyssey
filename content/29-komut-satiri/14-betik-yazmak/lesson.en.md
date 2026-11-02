# Writing Scripts

If you type the same commands again every day, it is time to put them in a
file. A **script** is commands written into a file; when you run the file, the
commands run in order from top to bottom. In this section everything you have
learned so far (variables, redirection, pipes, permissions) comes together.

## The first script

<figure class="fig">
  <pre><code class="language-text">#!/bin/bash
# Greets the person given as the first argument.
echo "Hello, &#36;1!"</code></pre>
  <div class="anat">
    <div class="anat-row"><span>#!/bin/bash</span><span>The <b>shebang</b>: the first line. It says "run this file with bash".</span></div>
    <div class="anat-row"><span># ...</span><span>A comment: the shell skips a line starting with <code>#</code>.</span></div>
    <div class="anat-row"><span>echo ...</span><span>Commands: the same ones you would type in the terminal, in order from top to bottom.</span></div>
    <div class="anat-row"><span>&#36;1</span><span>The first argument given to the script.</span></div>
  </div>
  <figcaption>A script is commands written into a file. You are not learning something new; you are saving what you know.</figcaption>
</figure>

```text
~ $ cat hello.sh
#!/bin/bash
# My first script
echo "Hello from a script"
echo "I am running in $PWD"
~ $ bash hello.sh
Hello from a script
I am running in /home/ada
~ $ ./hello.sh
bash: ./hello.sh: Permission denied
~ $ chmod +x hello.sh
~ $ ./hello.sh
Hello from a script
I am running in /home/ada
```

- `bash hello.sh`: bash read the file and ran the commands in it. Being able to
  read the file is enough for that.
- `./hello.sh`: running the file **as a program**. Remember from the
  Permissions section: that needs the `x` permission; after `chmod +x` it ran.
- When run with `./hello.sh`, the first line, the **shebang**
  (`#!/bin/bash`), says which program to use.

On a real computer you write a script in an editor (VS Code, nano). This
terminal has no editor; the scripts come ready, and you will write your own
script line by line with `echo` and `>>`.

## Arguments

<figure class="fig">
  <pre><code class="language-text">./greet.sh Ada Grace Linus</code></pre>
  <div class="anat">
    <div class="anat-row"><span>&#36;0</span><span>The script's own name: <code>./greet.sh</code></span></div>
    <div class="anat-row"><span>&#36;1 &#36;2 &#36;3</span><span>The arguments in order: <code>Ada</code>, <code>Grace</code>, <code>Linus</code></span></div>
    <div class="anat-row"><span>&#36;#</span><span>The number of arguments: <code>3</code></span></div>
    <div class="anat-row"><span>&#36;@</span><span>All the arguments; used in quotes as <code>"&#36;@"</code></span></div>
  </div>
  <figcaption>Arguments let you use the script with a different value each time you run it.</figcaption>
</figure>

```text
~ $ bash greet.sh Ada
Hello, Ada!
You gave 1 arguments: Ada
This script is greet.sh
~ $ bash greet.sh Ada Grace Linus
Hello, Ada!
You gave 3 arguments: Ada Grace Linus
This script is greet.sh
~ $ bash greet.sh "Ada Lovelace"
Hello, Ada Lovelace!
You gave 1 arguments: Ada Lovelace
This script is greet.sh
~ $ bash greet.sh
Hello, !
You gave 0 arguments: 
This script is greet.sh
```

- `"Ada Lovelace"` was counted as **one** argument because it is in quotes.
- Without an argument `$1` stayed empty and the script still ran:
  `Hello, !`. Preventing that is the job of the next topic.

## Making decisions: if

```text
~ $ cat check.sh
#!/bin/bash
if [ -z "$1" ]; then
  echo "usage: check.sh FILE"
  exit 1
fi
if [ -f "$1" ]; then
  lines=$(wc -l < "$1")
  echo "$1 has $lines lines"
else
  echo "$1: no such file"
  exit 2
fi
~ $ bash check.sh
usage: check.sh FILE
~ $ bash check.sh notes.txt
notes.txt has 3 lines
~ $ bash check.sh nope.txt
nope.txt: no such file
```

```text
if [ condition ]; then
  commands
else
  other commands
fi
```

- `[ -z "$1" ]`: is the first argument empty? If so, print the usage and leave
  with `exit 1`. The rest of the script never ran.
- `[ -f "$1" ]`: does such a file exist?
- `exit` ends the script; the number after it is the **exit code**. 0 means
  "success", every other number "something is wrong". Exit codes are the next
  section's topic.

`[ ... ]` is actually a command (`test`), and there **must be spaces inside**
the brackets. It works on the command line too:

```text
~ $ [ -f notes.txt ] && echo file
file
~ $ [ -d notes.txt ] || echo not a folder
not a folder
~ $ [ 3 -gt 2 ] && echo bigger
bigger
~ $ name=Ada
~ $ if [ "$name" = "Ada" ]; then echo hi Ada; else echo who; fi
hi Ada
```

| Test | True if |
|---|---|
| `-f path` / `-d path` / `-e path` | A file / folder / either exists |
| `-z "$a"` / `-n "$a"` | The text is empty / not empty |
| `"$a" = "$b"` / `"$a" != "$b"` | The texts are equal / different |
| `$a -eq $b`, `-ne`, `-lt`, `-le`, `-gt`, `-ge` | Number comparison |
| `! ...` | The opposite |

For numbers you use short forms like `-gt`; inside the brackets `>` is a
redirection and creates a file named `0`.

## Repeating: for and while

```text
~ $ for name in Ada Grace Linus; do echo "Hi, $name"; done
Hi, Ada
Hi, Grace
Hi, Linus
~ $ for f in *.txt; do echo "file: $f"; done
file: notes.txt
file: todo.txt
~ $ cat backup.sh
#!/bin/bash
for f in "$@"; do
  cp "$f" "$f.bak"
  echo "saved $f.bak"
done
~ $ bash backup.sh notes.txt todo.txt
saved notes.txt.bak
saved todo.txt.bak
~ $ ls *.bak
notes.txt.bak  todo.txt.bak
```

```text
for variable in list; do
  commands
done
```

The list can be plain words, a wildcard (`*.txt`), `"$@"` (all the arguments)
or a command's output (`$(seq 1 5)`). `backup.sh` made a copy of every file it
was given.

```text
~ $ cat countdown.sh
#!/bin/bash
n=$1
while [ $n -gt 0 ]; do
  echo $n
  n=$((n - 1))
done
echo "Go!"
~ $ bash countdown.sh 3
3
2
1
Go!
~ $ for i in $(seq 1 3); do touch "day$i.txt"; done
~ $ ls day*
day1.txt  day2.txt  day3.txt
```

`while` loops as long as the condition is true. `n=$((n - 1))` lowers the
number on every round; if you forget to lower it, the loop never ends. Short
loops need no script; they can be written on one line at the command line too.

## Functions

```text
~ $ cat report.sh
#!/bin/bash
count_lines() {
  local file=$1
  wc -l < "$file"
}
for f in *.txt; do
  echo "$f: $(count_lines "$f") lines"
done
~ $ bash report.sh
notes.txt: 3 lines
todo.txt: 1 lines
```

A function gives a name to a group of commands: `count_lines() { ... }`. When
called it takes arguments like any other command, and inside they become `$1`,
`$2`. `local` makes the variable belong to the function; it does not touch a
variable with the same name outside.

## Writing your own script

```text
~ $ echo '#!/bin/bash' > hi.sh
~ $ echo 'echo "Hi there"' >> hi.sh
~ $ cat hi.sh
#!/bin/bash
echo "Hi there"
~ $ chmod +x hi.sh
~ $ ./hi.sh
Hi there
```

We wrote the lines in single quotes: single quotes pass `!` and the inner
double quotes into the file as they are. The first line opened the file with
`>`, the next ones were added with `>>`.

## Traps

```text
~ $ hello.sh
bash: hello.sh: command not found
~ $ bash countdown.sh
countdown.sh: line 3: [: -gt: unary operator expected
Go!
~ $ bash nope.sh
bash: nope.sh: No such file or directory
```

- `hello.sh` alone cannot be found: the shell looks for commands in PATH, and
  the current folder is not in PATH. `./hello.sh` means "the file here".
- Without an argument `$n` stayed empty; `[ -gt 0 ]` became an incomplete
  test. The script gave an error but **did not stop**; `Go!` was still printed.
  Check the arguments or give a default: `n=${1:-3}`.
- Always use variables in double quotes: `"$1"`, `"$f"`. A file name with
  spaces is split into two words without quotes.

In a real terminal `bash -x script.sh` prints each command with `+` before
running it; the easiest way to see where a script goes wrong. `case` (a
decision with many options) and `read` (reading input from the keyboard) are
also common in scripts; this terminal does not have them.

## Summary

| Part | Form |
|---|---|
| First line | `#!/bin/bash` |
| Running | `bash script.sh` or `chmod +x` + `./script.sh` |
| Arguments | `$1`, `$2`, `$#`, `"$@"`, `$0` |
| Decision | `if [ ... ]; then ... else ... fi` |
| Loop | `for x in ...; do ... done`, `while [ ... ]; do ... done` |
| Function | `name() { ...; }`, `local` inside |
| Ending | `exit 0` success, `exit 1` a problem |
