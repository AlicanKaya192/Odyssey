# Finding Files with find

A project has hundreds of files and nested folders. Questions like "where was
that settings file?", "how many Python files does this project have?" or "I
want to delete all the backup files" are answered by `find`. `ls` only looks
inside a single folder; `find` goes into **every subfolder** from where it
starts.

The project we work with in this section looks like this: the `project` folder
holds source code (`src`), tests (`tests`), documents (`docs`), old backups
(`build`) and log files (`logs`).

<figure class="fig">
  <pre><code class="language-text">find project -type f -name '*.py'</code></pre>
  <div class="anat">
    <div class="anat-row"><span>find</span><span>The command: goes into the folder and all its subfolders.</span></div>
    <div class="anat-row"><span>project</span><span><b>Where</b> to start. Paths come first; <code>.</code> is the current folder.</span></div>
    <div class="anat-row"><span>-type f</span><span>A <b>condition</b>: files only (<code>d</code> for folders).</span></div>
    <div class="anat-row"><span>-name '*.py'</span><span>A <b>condition</b>: names that fit this pattern. The pattern goes in quotes.</span></div>
  </div>
  <figcaption>All conditions must hold ("and"). With no condition find prints everything.</figcaption>
</figure>

## Listing everything

```text
~ $ find project
project
project/build
project/build/main.bak
project/build/numbers.bak
project/docs
project/docs/guide.md
project/docs/notes.MD
project/empty
project/logs
project/logs/run1.log
project/logs/run2.log
project/readme.md
project/src
project/src/main.py
project/src/utils
project/src/utils/numbers.py
project/src/utils/text.py
project/tests
project/tests/test_main.py
~ $ find project -type d
project
project/build
project/docs
project/empty
project/logs
project/src
project/src/utils
project/tests
```

With no condition, `find project` prints the folder itself and everything
below it, each on its own line, with its **full path**. `-type d` keeps only
the folders; the empty `empty` folder is in the list too.

This terminal prints the results in alphabetical order. On a real Linux system
`find` prints files in the order they are stored on disk; the order can be
different, the result is the same. If you want them sorted, add `| sort`.

## By name: `-name` and `-iname`

```text
~ $ find project -name '*.py'
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
~ $ find project -name 'main*'
project/build/main.bak
project/src/main.py
~ $ find project -name '*.md'
project/docs/guide.md
project/readme.md
~ $ find project -iname '*.md'
project/docs/guide.md
project/docs/notes.MD
project/readme.md
```

- `-name '*.py'` found everything whose name ends in `.py`, at any depth.
- `'main*'` found both `main.py` and the backup `main.bak`.
- `-name` cares about upper and lower case: the pattern `'*.md'` did not find
  `notes.MD`. `-iname` (*insensitive*) turns the difference off.

The pattern is the same wildcard pattern as in the Wildcards section (`*`, `?`,
`[ ]`); the difference is that `find` applies it, not the shell.

## By type and depth

```text
~ $ find project -type f -name '*.log'
project/logs/run1.log
project/logs/run2.log
~ $ find project/src -type f
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
~ $ find project -maxdepth 1
project
project/build
project/docs
project/empty
project/logs
project/readme.md
project/src
project/tests
~ $ find project/docs -type f -not -name '*.md'
project/docs/notes.MD
```

- `-type f` a file, `-type d` a folder. When you write several conditions,
  **all** must hold: "it is a file and its name ends in `.log`".
- The start path can be narrowed: `find project/src` only looks under `src`.
- `-maxdepth 1` does not go into subfolders; like `ls`, but the folder itself
  is in the list and the paths are full.
- `-not` (or `!`) turns a condition around: the only file in `docs` not ending
  in `.md` is `notes.MD`.

## Put the pattern in quotes

```text
~ $ find project -name *.py
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
~ $ touch setup.py
~ $ find project -name *.py
~ $ find project -name '*.py'
project/src/main.py
project/src/utils/numbers.py
project/src/utils/text.py
project/tests/test_main.py
```

The first command worked even without quotes, because there was no file ending
in `.py` in the current folder and the shell left `*.py` alone. Once `setup.py`
existed, the shell turned `*.py` into `setup.py` **before find ran**; find
searched only for a file named exactly `setup.py` and found nothing. It gave no
error either: this is the sneakiest kind of mistake. Always put the pattern in
quotes.

## In a pipe and in a file

```text
~ $ find project -name '*.py' | wc -l
4
~ $ find project -type f | grep test
project/tests/test_main.py
~ $ find . -name '*.log' > logs.txt
~ $ cat logs.txt
./project/logs/run1.log
./project/logs/run2.log
```

Because find writes each path on its own line, it combines with every tool from
the earlier sections: `wc -l` counts, `grep` filters, `>` saves. `find .`
starts from the current folder; the paths start with `./`.

## Running a command on every file found: `-exec`

```text
~ $ find project -name '*.log' -exec wc -l {} \;
2 project/logs/run1.log
2 project/logs/run2.log
~ $ find project -name '*.py' -exec grep -l TODO {} \;
project/src/main.py
project/src/utils/numbers.py
```

`-exec` runs a command for **every** path found. `{}` stands for the current
path, `\;` says the command has ended (the backslash makes `;` go to find
instead of the shell). The second command joins two tools: find chose the
files named `.py`, and `grep -l` printed the names of those containing `TODO`.

## Deleting: `-delete`

```text
~ $ find project -name '*.bak'
project/build/main.bak
project/build/numbers.bak
~ $ find project -name '*.bak' -delete
~ $ find project -name '*.bak'
~ $ ls project/build
```

`-delete` deletes everything it finds **without asking and for good**. That is
why the routine is always the same:

1. Run the command without `-delete` and look at the list.
2. If the list is exactly what you want, add `-delete` to the **end** of the
   same command.
3. Run it once more without `-delete` and see that it comes back empty.

The `build` folder stayed; only the two backups inside it are gone.

## Error messages

```text
~ $ find nope
find: 'nope': No such file or directory
~ $ find project -type x
find: Unknown argument to -type: x
~ $ find -name '*.py' project
find: paths must precede expression: `project'
find: possible unquoted pattern after predicate `-name'?
```

- The start path must exist.
- `-type` only knows certain letters (`f`, `d`...).
- The path is written **before** the conditions. find gives a hint here as
  well: it thinks the pattern may have been left without quotes.

In a real terminal find also searches by size (`-size +1M`), by date
(`-mtime -7`: changed in the last 7 days) and by emptiness (`-empty`); to join
conditions with "or" there is `-o`. This terminal does not have them.

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>ls</h4><p>Inside one folder</p><p>Names and details</p></div>
    <div class="ok"><h4>find</h4><p>Every subfolder</p><p>Searches by the <b>file's name</b> and type</p></div>
    <div class="ok"><h4>grep -r</h4><p>Every subfolder</p><p>Searches by <b>what is inside</b> the file</p></div>
  </div>
  <figcaption>"What was it called?" is a question for find; "what did it say inside?" is one for grep.</figcaption>
</figure>

## Summary

| Form | What it finds |
|---|---|
| `find path` | Everything under the path |
| `find path -name 'p'` | Names that fit the pattern p |
| `find path -iname 'p'` | The same, ignoring upper/lower case |
| `find path -type f` / `-type d` | Files / folders |
| `find path -maxdepth 1` | Without going into subfolders |
| `find path -not -name 'p'` | Those that do not fit |
| `find path ... -exec command {} \;` | A command on each match |
| `find path ... -delete` | Deletes the matches (list them first!) |

The path first, then the conditions; the pattern in quotes.
