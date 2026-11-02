# Looking Closer with ls

So far we have used `ls` only to see names. But `ls` can tell you much more
about a file: how big it is, when it last changed, who owns it, who can read
and write it. In this section we learn the most used options of `ls` and
every column of the long listing.

## A reminder: plain `ls`

```text
~/project $ ls
data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -1
data.csv
docs/
notes.txt
report.txt
src/
```

Plain `ls` puts the names side by side. `-1` (the digit one) writes each name
on its own line; it is easier to read in long lists.

## The long listing: `ls -l`

The `-l` (*long*) option prints one line for each file:

```text
~/project $ ls -l
total 588
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada      0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 src/
```

The line looks complicated at first, but it is always made of the same
columns:

<figure class="fig">
  <pre><code class="language-text">-rw-r--r-- 1 ada ada  412 Oct  7 10:00 report.txt</code></pre>
  <div class="anat">
    <div class="anat-row"><span>-</span><span>Type: <code>-</code> a regular file, <code>d</code> a folder (directory).</span></div>
    <div class="anat-row"><span>rw-r--r--</span><span>Permissions: who can read, write, run it. Details in the Permissions section.</span></div>
    <div class="anat-row"><span>1</span><span>Link count. Usually 1 for a file; skip it for now.</span></div>
    <div class="anat-row"><span>ada</span><span>The owner (user).</span></div>
    <div class="anat-row"><span>ada</span><span>The group.</span></div>
    <div class="anat-row"><span>412</span><span>Size in bytes. With <code>-h</code> it reads like 4.0K.</span></div>
    <div class="anat-row"><span>Oct  7 10:00</span><span>Last modification time.</span></div>
    <div class="anat-row"><span>report.txt</span><span>The name.</span></div>
  </div>
  <figcaption><code>ls -l</code> (long) prints one line per file; the columns are always in this order.</figcaption>
</figure>

The three things you will look at most: **the first character** (file or
folder), **the size** and **the name**. We will read the permissions column
letter by letter in the Permissions section; for now, know that `rw-` means
"can be read and written".

A few details:

- The size of `notes.txt` is `0`: an empty file created with `touch`.
- Folders have size `4096`. This is not the total of what is inside; it is
  the one disk block the folder's own entry takes.
- The `total` line at the top is not the number of files; it is the total
  disk space the files take, in blocks. It is usually ignored.

## Readable sizes: `-h`

How many megabytes is `588895`? Hard to work out. `-h` (*human-readable*)
writes sizes with the units `K`, `M`, `G`:

```text
~/project $ ls -l data.csv report.txt
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
~/project $ ls -lh data.csv report.txt
-rw-r--r-- 1 ada ada 576K Oct  7 10:00 data.csv
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
~/project $ ls -lh
total 588K
-rw-r--r-- 1 ada ada 576K Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada 4.0K Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada    0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada 4.0K Oct  7 10:00 src/
```

`576K` means about half a megabyte (1 K = 1024 bytes, 1 M = 1024 K). Files
smaller than 1024 bytes stay as they are (`292`). The order of the option
letters does not matter: `ls -lh`, `ls -hl` and `ls -l -h` are the same.

## With hidden files: `-a` and `-A`

```text
~/project $ ls -a
./  ../  .env  data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -A
.env  data.csv  docs/  notes.txt  report.txt  src/
~/project $ ls -la
total 600
drwxr-xr-x 4 ada ada   4096 Oct  7 10:00 ./
drwxr-xr-x 3 ada ada   4096 Oct  7 10:00 ../
-rw-r--r-- 1 ada ada      6 Oct  7 10:00 .env
-rw-r--r-- 1 ada ada 588895 Oct  7 10:00 data.csv
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 docs/
-rw-r--r-- 1 ada ada      0 Oct  7 10:00 notes.txt
-rw-r--r-- 1 ada ada    292 Oct  7 10:00 report.txt
drwxr-xr-x 2 ada ada   4096 Oct  7 10:00 src/
```

- `-a` (*all*) shows hidden files and the `./` and `../` entries.
- `-A` (*almost all*) shows hidden files but leaves out `./` and `../`.
- `-la` combines both: hidden files included, in detail. The most common way
  to look at "what is in this folder, all of it".

## With all subfolders: `-R`

`-R` (*recursive*, a capital letter) lists the folder and every folder inside
it, one after another. Before each folder it prints its path as a header:

```text
~ $ ls -R project
project:
data.csv  docs/  notes.txt  report.txt  src/

project/docs:
readme.md

project/src:
main.py
```

In big projects `-R` gives a very long output; for finding files we will meet
a much better tool later: `find`.

## The folder itself: `-d`

If you give `ls` a folder, it looks **inside** it. To see the folder's own
line, add `-d` (*directory*):

```text
~ $ ls -l project/src
total 4
-rw-r--r-- 1 ada ada 9 Oct  7 10:00 main.py
~ $ ls -ld project/src
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 project/src/
~ $ ls -l project/src/main.py
-rw-r--r-- 1 ada ada 9 Oct  7 10:00 project/src/main.py
```

If you give it a file, `ls` prints just that file's line.

## Summary

| Command | What it shows |
|---|---|
| `ls -1` | Each name on its own line |
| `ls -l` | Type, permissions, owner, group, size, date, name |
| `ls -lh` | Sizes with `K`, `M`, `G` |
| `ls -a` | Hidden files and `./`, `../` |
| `ls -A` | Hidden files, without `./` and `../` |
| `ls -la` | Hidden files included, in detail |
| `ls -R` | With all subfolders |
| `ls -ld folder` | The folder's own line |

Options combine (`-lah`) and their order does not matter.
