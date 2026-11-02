# Searching Text with grep

A log file can have thousands of lines and you want to see only the error
lines. In a project you want to find which files mention a function's name.
The answer to both is `grep`. Its name comes from an old editor command
(*global regular expression print*); today it is one of the most used tools on
the command line.

## Filtering lines

<figure class="fig">
  <pre><code class="language-text">grep -i -n error logs/app.log</code></pre>
  <div class="anat">
    <div class="anat-row"><span>grep</span><span>The command: reads line by line and prints the lines that carry the pattern.</span></div>
    <div class="anat-row"><span>-i -n</span><span>Options: ignore upper/lower case, print the line number.</span></div>
    <div class="anat-row"><span>error</span><span>The <b>pattern</b>: the text to look for. Always the first argument.</span></div>
    <div class="anat-row"><span>logs/app.log</span><span>The file(s) to search. Without them grep reads its input (a pipe).</span></div>
  </div>
  <figcaption>The pattern first, then the files. Everything after the pattern is taken as a file name.</figcaption>
</figure>

```text
~ $ grep ERROR logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
~ $ grep database logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:06 INFO retrying database
2026-10-07 10:07 info database ok
~ $ grep nothing logs/app.log
~ $ echo $?
1
```

`grep` reads the file line by line and prints the lines that carry the pattern
**as they are**. If it finds no line it prints nothing, but the exit code tells
you:

- `0`: it found at least one line,
- `1`: it found none,
- `2`: something went wrong (like a missing file).

In scripts, the question "does this file have errors?" is asked with this code.

## Upper and lower case: `-i`

```text
~ $ grep error logs/app.log
~ $ grep -i error logs/app.log
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:13 Error timeout while sending mail
```

`grep` is **case sensitive**: searching for `error` does not find `ERROR`.
`-i` (*ignore case*) turns the difference off; all forms (`ERROR`, `Error`)
were found. In real log files the spelling is often inconsistent, which is why
`-i` is used very often.

## Number, count, opposite: `-n`, `-c`, `-v`

```text
~ $ grep -n WARN logs/app.log
3:2026-10-07 10:03 WARN slow request /books
7:2026-10-07 10:08 WARN disk 85% full
11:2026-10-07 10:14 WARN disk 90% full
~ $ grep -c INFO logs/app.log
5
~ $ grep -v INFO logs/app.log
2026-10-07 10:03 WARN slow request /books
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:07 info database ok
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:13 Error timeout while sending mail
2026-10-07 10:14 WARN disk 90% full
```

- `-n` puts each line's number in front of it (`3:`). Useful for opening the
  file in an editor and jumping to that line.
- `-c` does not print the lines, it **counts** them. The same result as
  `grep INFO file | wc -l`.
- `-v` does the opposite: it prints the lines that do **not** carry the
  pattern. Here everything except `INFO` came out; note that the lower-case
  `info` line came too.

## Part of a word, a whole word: `-w`, `-x`

```text
~ $ grep -c in logs/app.log
5
~ $ grep -w in logs/app.log
2026-10-07 10:01 INFO user ada logged in
2026-10-07 10:11 INFO user alan logged in
~ $ grep -x ada names.txt
ada
```

`grep -c in` counted five lines: besides `logged in`, the words `info`, `retrying`
and `sending` also carry the letters `in`. The pattern is searched as a **piece
of text**. `-w` (*word*) finds only the word standing on its own. `-x` is even
stricter: the **whole** line must equal the pattern.

## Patterns: regular expressions

grep's pattern is not plain text but a **regular expression**. Some characters
have a special meaning:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>^a</code></span><span>Lines that <b>start</b> with <code>a</code>.</span></div>
    <div class="anat-row"><span><code>e$</code></span><span>Lines that <b>end</b> with <code>e</code>.</span></div>
    <div class="anat-row"><span><code>.</code></span><span>Any <b>single</b> character.</span></div>
    <div class="anat-row"><span><code>[0-9]</code></span><span>One of the characters in the brackets: here a digit.</span></div>
    <div class="anat-row"><span><code>x*</code></span><span>Zero or more of the character before it.</span></div>
    <div class="anat-row"><span><code>-E 'A|B'</code></span><span>A <b>or</b> B (extended expression; <code>+</code> means "one or more").</span></div>
  </div>
  <figcaption>The pattern is a <b>regular expression</b>. It looks like wildcards but is not the same: here <code>.</code> is one character and <code>*</code> means "repeat the one before".</figcaption>
</figure>

```text
~ $ grep '^a' names.txt
ada
alan
~ $ grep 'e$' names.txt
grace
katherine
~ $ grep 'disk ..% full' logs/app.log
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:14 WARN disk 90% full
~ $ grep -E 'ERROR|WARN' logs/app.log
2026-10-07 10:03 WARN slow request /books
2026-10-07 10:05 ERROR database timeout
2026-10-07 10:08 WARN disk 85% full
2026-10-07 10:10 ERROR payment failed
2026-10-07 10:14 WARN disk 90% full
~ $ grep -oE '[0-9]+%' logs/app.log
85%
90%
```

- `'^a'`: names starting with `a`. `'e$'`: names ending with `e`.
- `'disk ..% full'`: two dots mean any two characters; both 85 and 90 fit.
- `-E 'ERROR|WARN'`: `-E` turns on the extended expression and `|` becomes
  "or".
- `-o` prints only the **matching part**, not the whole line. `[0-9]+` means
  "one or more digits".

Do not mix them up with wildcards: in the Wildcards section `*` meant "any
text" and the shell did the work. In a regular expression `*` means "zero or
more of the character before it"; "any text" is written `.*`.

## Several files and folders: `-r`, `-l`

```text
~ $ grep -c ERROR logs/app.log logs/old/2025.log
logs/app.log:2
logs/old/2025.log:1
~ $ grep -r ERROR logs
logs/app.log:2026-10-07 10:05 ERROR database timeout
logs/app.log:2026-10-07 10:10 ERROR payment failed
logs/old/2025.log:2025-12-31 23:55 ERROR disk full
~ $ grep -rl ERROR logs
logs/app.log
logs/old/2025.log
```

- With several files, grep puts the **file name** in front of each line.
- `-r` (*recursive*) goes into the folder and its subfolders.
- `-l` prints only the **names of the files** that have a match, not the
  lines. It answers the question "which files mention this word?".

## grep in a pipe

Without a file name grep reads its input; that is why it is the most common
part of pipelines:

```text
~ $ ls docs | grep txt
d.txt
e.txt
~ $ grep -i error logs/app.log | wc -l
3
~ $ grep -ic error logs/app.log
3
```

Short options can be combined: `-ic` instead of `-i -c`. The last two commands
gave the same number.

## Use quotes

```text
~ $ grep user ada logs/app.log
grep: ada: No such file or directory
logs/app.log:2026-10-07 10:01 INFO user ada logged in
logs/app.log:2026-10-07 10:11 INFO user alan logged in
~ $ echo $?
2
~ $ grep 'user ada' logs/app.log
2026-10-07 10:01 INFO user ada logged in
```

Without quotes the shell split at the space: the pattern became only `user`,
and `ada` was taken as a **file name**. grep could not find the file `ada`
(exit code 2) and printed every line containing `user`. Always write the
pattern in single quotes; that way characters like `$`, `*` and `|` reach grep
instead of the shell.

## Summary

| Option | What it does |
|---|---|
| `-i` | Ignore upper/lower case |
| `-n` | Line numbers |
| `-c` | A count |
| `-v` | The non-matching lines |
| `-w` / `-x` | Whole word / whole line |
| `-o` | Only the matching part |
| `-E` | Extended expression (`+`, "or") |
| `-r` / `-l` | Subfolders / only file names |

The pattern first, then the files; the pattern in single quotes. Exit code 0
found, 1 not found, 2 error.
