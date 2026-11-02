# Looking Inside Files

So far we have used `cat` to see what is inside a file. That is enough for
short files; but a server's log file can have thousands of lines, and dumping
all of them on the screen shows you nothing. In this section we learn to look
at **part of** a file and to **count** a file: `head`, `tail`, `wc`, and
`less` from real terminals.

The examples use two files: a short poem (`poem.txt`) and a server's log file
(`logs/server.log`). A log file is a file in which a program writes what it
does, line by line, with the time.

## All of it: `cat`

```text
~ $ cat poem.txt
Roses are red
Violets are blue
The shell is fast
And so are you
~ $ cat -n poem.txt
     1  Roses are red
     2  Violets are blue
     3  The shell is fast
     4  And so are you
```

`cat -n` puts a number at the start of each line. Useful when you look at a
file with information like "the error is on line 3".

Even a fifteen-line log file takes quite a lot of space on the screen:

```text
~ $ cat logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
2026-10-07 10:03 WARN slow request /api/books
2026-10-07 10:04 INFO user alan logged in
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 INFO database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:09 INFO user grace logged in
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:11 INFO backup done
2026-10-07 10:12 INFO user ada logged out
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
```

In a thousand-line file the first lines would long have scrolled off the top
of the screen. Most of the time you do not want the whole file, only its
start or its end.

## Start and end: `head` and `tail`

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>head</h4><p>10 lines from the start</p><p><code>head -n 3</code>: the first 3</p><p>How does the file start?</p></div>
    <div class="ok"><h4>tail</h4><p>10 lines from the end</p><p><code>tail -n 3</code>: the last 3</p><p><code>tail -n +5</code>: from line 5 to the end</p></div>
  </div>
  <figcaption>Instead of dumping a whole big file on the screen you look at its start or end. In log files the newest lines are at the end.</figcaption>
</figure>

`head` prints the start of a file; **10** lines without options. With `-n` you
say how many lines you want (instead of `-n 3` you can also write `-3`):

```text
~ $ head logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
2026-10-07 10:03 WARN slow request /api/books
2026-10-07 10:04 INFO user alan logged in
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 INFO database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:09 INFO user grace logged in
~ $ head -n 3 logs/server.log
2026-10-07 10:00 INFO server started
2026-10-07 10:01 INFO listening on port 8080
2026-10-07 10:02 INFO user ada logged in
~ $ head -3 poem.txt
Roses are red
Violets are blue
The shell is fast
```

`tail` does the same from the end. If you put `+` in front of the number, the
meaning changes: not "the last N lines" but "from line N to the end":

```text
~ $ tail -n 3 logs/server.log
2026-10-07 10:12 INFO user ada logged out
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
~ $ tail -n +14 logs/server.log
2026-10-07 10:13 WARN disk 90% full
2026-10-07 10:14 INFO server stopped
~ $ tail -n 1 poem.txt logs/server.log
==> poem.txt <==
And so are you

==> logs/server.log <==
2026-10-07 10:14 INFO server stopped
```

With several files, `head` and `tail` put a `==> name <==` header before each
file, so you can tell which line came from which file.

In log files the newest lines are **at the end**, because programs add to the
end of the file. The first answer to "what just happened?" is `tail`. In a
real terminal, `tail -f server.log` (*follow*) keeps watching the file and
prints new lines as they arrive; it stops with `Ctrl+C`. Files do not grow by
themselves in this terminal, so there is no `-f` here.

## Counting: `wc`

`wc` (*word count*) counts the lines, words and bytes of a file:

<figure class="fig">
  <pre><code class="language-text"> 15  88 591 logs/server.log</code></pre>
  <div class="anat">
    <div class="anat-row"><span>15</span><span>Number of lines (<code>-l</code>, lines).</span></div>
    <div class="anat-row"><span>88</span><span>Number of words (<code>-w</code>, words): pieces separated by spaces.</span></div>
    <div class="anat-row"><span>591</span><span>Number of bytes (<code>-c</code>): the file's size, line endings included.</span></div>
    <div class="anat-row"><span>logs/server.log</span><span>The file that was counted.</span></div>
  </div>
  <figcaption><code>wc</code> (word count) prints all three without options; with an option, only the one you ask for.</figcaption>
</figure>

```text
~ $ wc logs/server.log
 15  88 591 logs/server.log
~ $ wc -l logs/server.log
15 logs/server.log
~ $ wc -w poem.txt
14 poem.txt
~ $ wc -c poem.txt
64 poem.txt
~ $ wc -l poem.txt logs/server.log
  4 poem.txt
 15 logs/server.log
 19 total
```

- `wc -l` is the line count only. This is the one used most: "how many lines
  are in the log", "how many people are on the list".
- `wc -w` counts words, `wc -c` bytes. The byte count is the same as the size
  in `ls -l`.
- With several files a `total` line is added at the end.

`wc` gives you the result without showing the file. It is the way to answer
"how big is it" without dumping the file on the screen.

## Errors

```text
~ $ head -n ten poem.txt
head: invalid number of lines: 'ten'
~ $ tail nope.txt
tail: cannot open 'nope.txt' for reading: No such file or directory
~ $ wc logs
wc: logs: Is a directory
      0       0       0 logs
```

- The number of lines is written in digits: `-n 10`, not `-n ten`.
- When `head` and `tail` cannot find the file they say
  `cannot open ... for reading`.
- The inside of a folder cannot be read; after printing the error, `wc` still
  prints a line of zeros.

## Reading page by page: `less`

In a real terminal the most comfortable way to read a long file is `less`:

```text
$ less logs/server.log
```

`less` opens the file in a view that fills the screen; you move with the
arrow keys or the space bar, search by typing `/error`, and quit with `q`. It
does not change the file, it only shows it. (The name comes from a joke: an
older program was called *more*, and `less` does more than it.)

Odyssey's terminal cannot open full-screen programs, so there is no `less`
here; you will use `head`, `tail` and `cat -n` instead. The keys are in the
notes.

## Summary

| Command | What it does |
|---|---|
| `cat -n file` | The whole file, with line numbers |
| `head file` | The first 10 lines |
| `head -n 3 file` | The first 3 lines |
| `tail -n 3 file` | The last 3 lines |
| `tail -n +5 file` | From line 5 to the end |
| `wc file` | Lines, words, bytes |
| `wc -l file` | The line count only |
| `less file` | Reading page by page (in a real terminal) |
