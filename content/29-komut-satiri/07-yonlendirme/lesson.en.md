# Redirection: Sending Output to Files

In the Creating Files section we wrote `echo "text" > file`, and the text went
into the file instead of the screen. That was the first example of one of the
shell's most powerful features: **redirection**. You can send the output of
any command to a file, separate the error messages, or feed a command its
input from a file. In this section we go through all of them in order.

## Three streams

Every command has three **streams**. A stream can be thought of as a channel
that data flows through:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>0 stdin</span><span><b>Standard input</b>: where the command reads from. The keyboard by default; a file with <code>&lt;</code>.</span></div>
    <div class="anat-row"><span>1 stdout</span><span><b>Standard output</b>: the command's real result. The screen by default; a file with <code>&gt;</code>.</span></div>
    <div class="anat-row"><span>2 stderr</span><span><b>Standard error</b>: error messages. Also the screen by default; a file with <code>2&gt;</code>.</span></div>
  </div>
  <figcaption>Every command has three streams. On the screen stdout and stderr look mixed, but they are separate channels; redirection separates them.</figcaption>
</figure>

On the screen a command's output and its error messages appear one below the
other, but to the shell they come from different channels. Redirection
connects these channels to files instead of the screen.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>&gt; file</span><span>stdout into the file; the file is <b>written from the start</b>.</span></div>
    <div class="anat-row"><span>&gt;&gt; file</span><span>stdout is <b>added to the end</b> of the file.</span></div>
    <div class="anat-row"><span>2&gt; file</span><span>Only the error messages into the file.</span></div>
    <div class="anat-row"><span>&gt; file 2&gt;&amp;1</span><span>Both into the same file (first <code>&gt;</code>, then <code>2&gt;&amp;1</code>).</span></div>
    <div class="anat-row"><span>&amp;&gt; file</span><span>The short bash spelling of the same thing.</span></div>
    <div class="anat-row"><span>&lt; file</span><span>The command reads its input from the file instead of the keyboard.</span></div>
    <div class="anat-row"><span>/dev/null</span><span>The "nothing" file: everything sent here disappears.</span></div>
  </div>
  <figcaption>Redirection is written at the end of the command, and the command itself knows nothing about it; the shell does the work.</figcaption>
</figure>

## Output into a file: `>`

```text
~ $ ls notes
ideas.txt  todo.txt
~ $ ls notes > list.txt
~ $ cat list.txt
ideas.txt
todo.txt
~ $ date > today.txt
~ $ cat today.txt
Wed Oct  7 10:00:00 +03 2026
```

`ls notes > list.txt` printed nothing on the screen; the list went into the
file. In the file the names are on separate lines, because when the output of
`ls` goes to a file instead of the screen it writes each name on its own line.
The `date` command prints the current date; we could send that to a file too.
Redirection works with **every** command, because the shell does the work, not
the command.

## Adding to the end: `>>`

```text
~ $ echo "first run" > run.log
~ $ echo "second run" >> run.log
~ $ cat run.log
first run
second run
~ $ echo "oops" > run.log
~ $ cat run.log
oops
```

`>` writes the file from the start every time; `>>` adds to its end. For jobs
like noting every run of a script in a log file, `>>` is always used.

## Separating errors: `2>`

`>` only redirects stdout. Error messages come from stderr, so they stay on
the screen:

```text
~ $ ls notes nope
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt  todo.txt
~ $ ls notes nope > out.txt
ls: cannot access 'nope': No such file or directory
~ $ cat out.txt
notes:
ideas.txt
todo.txt
~ $ ls notes nope 2> errors.txt
notes:
ideas.txt  todo.txt
~ $ cat errors.txt
ls: cannot access 'nope': No such file or directory
```

- `> out.txt` wrote the list into the file; the error still showed on the
  screen.
- `2> errors.txt` wrote only the error into the file; the list stayed on the
  screen.

`2` is the number of stderr. `>` is really a short way of writing `1>`.

## Both at once: `2>&1` and `&>`

To collect the output and the errors in the **same** file, you first send
stdout to the file, then connect stderr to "wherever stdout goes":

```text
~ $ ls notes nope > all.txt 2>&1
~ $ cat all.txt
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt
todo.txt
~ $ ls notes nope &> all2.txt
~ $ cat all2.txt
ls: cannot access 'nope': No such file or directory
notes:
ideas.txt
todo.txt
```

`2>&1` means "send number 2 to where number 1 goes". The `&` in front tells
the shell that `1` is a stream number, not a file name; with `2>1` you would
create a file named `1`. The order matters: first `> file`, then `2>&1`. In
bash the short way to do the same is `&> file`.

## Sending to nowhere: `/dev/null`

`/dev/null` is a special file: everything written into it disappears, and
reading it gives nothing. You send output you do not want to see there:

```text
~ $ ls nope
ls: cannot access 'nope': No such file or directory
~ $ ls nope 2> /dev/null
~ $ ls notes > /dev/null
~ $ cat /dev/null
```

The command still ran and the exit code did not change; we just did not see
the message. In scripts, `2> /dev/null` is the way to say "do not print
errors on the screen".

## Input from a file: `<`

`<` works in the other direction: the command reads its input from a file
instead of the keyboard.

```text
~ $ sort names.txt
ada
alan
grace
linus
~ $ sort < names.txt
ada
alan
grace
linus
~ $ wc -l names.txt
4 names.txt
~ $ wc -l < names.txt
4
~ $ sort < names.txt > sorted.txt
~ $ cat sorted.txt
ada
alan
grace
linus
```

`sort names.txt` and `sort < names.txt` gave the same result: in one, `sort`
opened the file; in the other, the shell opened it and handed its content to
`sort`. The difference shows in `wc`: with `<`, `wc` does not know the file's
name, so it printed only the number. Very handy when you want to use the
number in a script. One line can have both `<` and `>`.

## Traps

```text
~ $ ls nope > empty.txt
ls: cannot access 'nope': No such file or directory
~ $ cat empty.txt
~ $ wc -c empty.txt
0 empty.txt
~ $ echo hi > nowhere/x.txt
bash: nowhere/x.txt: No such file or directory
~ $ echo hi > notes
bash: notes: Is a directory
```

- **The file is opened before the command runs.** `ls nope > empty.txt`
  failed, but `empty.txt` was still created, and it is empty. That is why you
  never write `sort names.txt > names.txt`: the shell empties `names.txt`
  before `sort` reads it, and the content is lost. Write the result to a
  different file.
- `>` does not create folders: if the target folder does not exist, **the
  shell** prints the error (`bash: ...`).
- You cannot write over a folder: `Is a directory`.

## Summary

| Spelling | What it does |
|---|---|
| `command > file` | stdout into the file, written from the start |
| `command >> file` | stdout to the end of the file |
| `command 2> file` | Only the errors into the file |
| `command > file 2>&1` | Both into the same file (`&> file`) |
| `command 2> /dev/null` | Throw the errors away |
| `command < file` | Read the input from the file |
| `command < input > output` | Both at once |

The shell does the redirection, so it works with every command. Never write
with `>` into the file you are reading in the same command.
