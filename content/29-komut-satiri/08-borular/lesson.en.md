# Pipes: Connecting Commands

In the Redirection section we sent a command's output to a **file**. In this
section we send the output to another **command**. The sign that does it is
`|`, called a **pipe**. This is what makes the command line truly powerful:
you join small commands, each doing one job well, end to end and build big
jobs out of them.

## The first pipe

```text
~ $ ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ ls docs | wc -l
5
~ $ cat names.txt
grace
ada
linus
alan
margaret
katherine
dennis
~ $ cat names.txt | sort
ada
alan
dennis
grace
katherine
linus
margaret
```

`ls docs | wc -l` ran two commands. `ls docs` gave the list it would have
printed to the pipe instead of the screen; `wc -l` read that list as its input
and counted the lines. The result: there are 5 files in `docs`. The second pipe works the same way: `cat` handed the names to
`sort` through the pipe, and `sort` sorted them.

<figure class="fig">
  <div class="flow">
    <span class="node">cat names.txt<br><small>prints 7 names</small></span><span class="arrow">→</span>
    <span class="node acc">sort<br><small>sorts them</small></span><span class="arrow">→</span>
    <span class="node acc">head -n 3<br><small>keeps the first 3</small></span><span class="arrow">→</span>
    <span class="node">Screen<br><small>ada, alan, dennis</small></span>
  </div>
  <figcaption>A pipe (<code>|</code>) connects the stdout of the command on the left to the stdin of the command on the right. The results in between are not written to any file.</figcaption>
</figure>

A pipe connects the **stdout** of the command on the left to the **stdin** of
the command on the right. Remember the streams from the Redirection section:
number 1 (stdout) flows into number 0 (stdin) of the next command. The results
in between are not written to any file.

## Building a chain

You can add as many commands to a pipeline as you like:

```text
~ $ cat names.txt | sort | head -n 3
ada
alan
dennis
~ $ sort names.txt | tail -n 2
linus
margaret
~ $ head -n 6 logs/app.log | tail -n 3
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 info database ok
```

- `cat names.txt | sort | head -n 3`: read, sort, keep the first three.
- `sort names.txt | tail -n 2`: `sort` can open the file itself; then the
  `cat` at the front is not needed.
- `head -n 6 logs/app.log | tail -n 3`: the last three of the first six lines,
  that is lines 4, 5 and 6 of the file. Neither `head` nor `tail` can do this
  alone; together they can.

When you build a chain, run it after each new `|` and look at the output. If a
step goes wrong you see at once which one it was.

## `ls` writes one column in a pipe

```text
~ $ ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ ls docs | cat
a.md
b.md
c.md
d.txt
e.txt
~ $ ls docs | head -n 2
a.md
b.md
```

On the screen `ls` lines the names up side by side. When its output goes into
a pipe (or a file) it writes each name on **its own line**, because the next
command reads line by line. That is why `ls docs | wc -l` gives the number of
files.

## Filtering: `grep` inside a pipe

`grep word` keeps the lines of its input that contain the word and throws the
others away. The details come in the next section; here we look at how it is
used in a pipe:

```text
~ $ ls docs | grep md
a.md
b.md
c.md
~ $ grep ERROR logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
~ $ grep ERROR logs/app.log | wc -l
2
```

`ls docs | grep md` kept only the names containing `md`. The last line is a
very common pattern: first **filter**, then **count**. This is how you find how
many errors a log file has.

## A pipe carries only stdout

```text
~ $ ls docs nope | wc -l
ls: cannot access 'nope': No such file or directory
6
~ $ ls docs nope 2>&1 | wc -l
7
~ $ ls docs nope 2> /dev/null | wc -l
6
```

- `ls docs nope | wc -l`: the error message still appeared on the screen and
  was not counted. `wc` said `6`: because two names were given, `ls` wrote the
  `docs:` heading first and then the five names.
- `2>&1 |`: first join stderr to stdout, then hand it to the pipe. The error
  line was counted too: `7`.
- `2> /dev/null |`: throw the error away, process only the list.

## Pipes and redirection together

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Pipe <code>|</code></h4><p>A <b>command</b> stands on its right</p><p><code>sort names.txt | head -n 3</code></p><p>The output goes to another program</p></div>
    <div class="ok"><h4>Redirection <code>&gt;</code></h4><p>A <b>file</b> stands on its right</p><p><code>sort names.txt &gt; sorted.txt</code></p><p>The output is written to a file</p></div>
  </div>
  <figcaption>They are also used together: process with pipes first, save with <code>&gt;</code> at the very end.</figcaption>
</figure>

```text
~ $ sort names.txt | head -n 3 > top.txt
~ $ cat top.txt
ada
alan
dennis
~ $ cat -n poem.txt | tail -n 2
     3  The shell is fast
     4  And so are you
```

`>` always catches the output of the command at the **end** of the line. In
the last command the order matters: `cat -n` numbered first and then `tail`
cut, so the numbers show the real positions in the poem (3 and 4).

In a real terminal you use `tee` to both see an output and save it:
`sort names.txt | tee sorted.txt` prints the result on the screen **and** saves
it to the file. This terminal has no `tee`; you do the same job with `> file`
followed by `cat file`.

## Traps

```text
~ $ echo names.txt | cat
names.txt
~ $ echo names.txt | ls docs
a.md  b.md  c.md  d.txt  e.txt
~ $ wc -l names.txt
7 names.txt
~ $ cat names.txt | wc -l
7
```

- **A pipe carries text, not a file name.** `echo names.txt | cat` prints the
  text `names.txt`, not what is inside the file.
- **Not every command reads its input.** `ls`, `cd` and `mkdir` ignore text
  coming from a pipe; `echo names.txt | ls docs` only lists `docs`, and the
  incoming text is lost.
- Text coming from a pipe has no name: `cat names.txt | wc -l` prints only the
  number.
- You do not write a file on the right of a pipe: `sort names.txt | top.txt`
  makes the shell look for a **program** named `top.txt`. A file needs `>`.

## Summary

- `command1 | command2`: the output of command1 becomes the input of command2.
- Only the last command's output (and errors) appear on the screen.
- In a pipe `ls` writes each name on its own line.
- A pipe does not carry stderr; to make it do so, `2>&1 |`.
- To save, put `> file` at the end of the line.
- Build the chain step by step and look at the output at each step.
