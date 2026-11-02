# Overall Review

In this path you went from opening a terminal to writing your own script. This
section uses all of it together: first we examine a small server log and a
messy folder from start to finish, then we gather the sections into a single
table. The quiz has 40 questions and there are five mixed exercises; each
exercise needs the tools of several sections together.

## A first look at a folder

```text
~ $ ls
inbox/  server.log  tools/
~ $ ls inbox
a.log  b.log  cache/  data.csv  draft.tmp  notes.txt  old.tmp
~ $ find . -type f | wc -l
10
~ $ find . -name '*.tmp'
./inbox/cache/page.tmp
./inbox/draft.tmp
./inbox/old.tmp
```

`ls` told us what is where, `find` how many files there are. The hidden
`.bashrc` in the home folder was counted too. The `.tmp` files are temporary:
you will clean them up in one of the exercises.

## Getting a summary out of a log

```text
~ $ wc -l server.log
16 server.log
~ $ grep -c ERROR server.log
6
~ $ grep ERROR server.log | cut -d ' ' -f 4- | sort | uniq -c | sort -rn
      3 db timeout
      2 disk full
      1 login failed
```

In three commands we learned the size of the log, how many errors it has and
how many times each error came. The last line is the most useful pattern of the
path: filter (`grep`), cut (`cut`), sort (`sort`), count (`uniq -c`), sort by
the count (`sort -rn`).

## Handing the job to a script

```text
~ $ cat tools/report.sh
#!/bin/bash
if [ ! -f "$1" ]; then
  echo "report: $1 not found"
  exit 2
fi
echo "$1: $(wc -l < "$1") lines, $(grep -c ERROR "$1") errors"
~ $ bash tools/report.sh server.log
server.log: 16 lines, 6 errors
~ $ bash tools/report.sh nope.log || echo "code: $?"
report: nope.log not found
code: 2
```

If you will ask the same question every day, write a script. `report.sh` checks
its argument and otherwise ends with its own exit code (2); `||` caught that.

## A map of the path

| Section | What to remember |
|---|---|
| Terminal, Shell and Prompt | The terminal is the window, the shell (bash) the program that runs commands |
| The File System and Paths | `pwd`, `cd`, `ls`; absolute (`/`) and relative paths, `~`, `..` |
| Creating Files and Folders | `mkdir -p`, `touch`, `rmdir`, `echo "..." > file` |
| Copying, Moving, Deleting | `cp -r`, `mv`, `rm`, `rm -r`; no recycle bin |
| Looking Closer with ls | `ls -l`, `-a`, `-h`, `-R` |
| Wildcards | `*`, `?`, `[ ]`, `{a,b}`; the shell expands them |
| Looking Inside Files | `cat`, `head`, `tail`, `wc` |
| Redirection | `>`, `>>`, `2>`, `2>&1`, `<`, `/dev/null` |
| Pipes | <code>a &#124; b</code>; `ls` is one column in a pipe |
| grep | `-i -n -c -v -w -o -E -r -l`, regular expressions |
| Text Tools | `sort`, `uniq`, `cut`, `tr` |
| find | `-name`, `-type`, `-maxdepth`, `-exec`, `-delete` |
| Permissions | `rwx`, `chmod +x`, `chmod 644/755/600` |
| Variables and the Environment | `name=value`, `"$name"`, `$( )`, `export`, PATH, `.bashrc` |
| Writing Scripts | shebang, `$1 $# "$@"`, `if`, `for`, `while`, functions |
| Exit Codes | `$?`, `&&`, <code>&#124;&#124;</code>, `exit`, processes |

## Three lessons that keep coming back

1. **Quotes.** Quote anything containing spaces, `*`, `$` or `|`. Single quotes
   expand nothing; double quotes expand variables.
2. **Look first, then change.** `rm`, `find -delete` and `>` cannot be undone.
   First see what will happen with `ls`, `find` or `cat`.
3. **Small pieces.** Build a pipeline or a script step by step; look at the
   output after each step.

The lesson notes contain a "Quick Reference" that gathers every command of the
path on one page, and "From Here", about what you can learn next.
