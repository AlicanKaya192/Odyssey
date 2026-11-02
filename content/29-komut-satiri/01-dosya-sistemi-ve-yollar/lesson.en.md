# The File System and Paths

To work with a file in the terminal, you first need to be able to say
**where** it is. In a graphical interface you click your way down through
folders; on the command line you do the same by writing a **path**. In this
section we look at how files are arranged, how paths are written and how to
move around with `cd`.

## A single tree

On Linux all files and folders live inside a single **tree**. The folder at
the very top of the tree is called the **root**, and its name is just the `/`
sign. Everything else is below it.

<figure class="fig">
  <pre><code class="language-text">/                     root: where everything starts
├── bin/              basic programs
├── etc/              the system's settings files
├── home/             users' folders
│   └── ada/          your home folder (~)
│       ├── notes/
│       └── projects/
│           ├── api/
│           └── site/
│               └── css/
├── root/             the administrator's (root's) home
├── tmp/              temporary files
├── usr/              programs and libraries
└── var/              changing data (logs)</code></pre>
  <figcaption>On Linux there is a single tree; its top is the root folder <code>/</code>. Every file has exactly one place in this tree.</figcaption>
</figure>

On Windows each disk has its own top (`C:`, `D:`); Linux has no drive
letters, everything is in the one tree under `/`. Let's go to the root folder
and look:

```text
~ $ cd /
/ $ pwd
/
/ $ ls
bin/  etc/  home/  root/  tmp/  usr/  var/
/ $ cd ~
~ $ pwd
/home/ada
~ $ ls
notes/  projects/
```

You do not need to know all the folders at the root; the ones you will meet
most often are:

- `/home`: the users' folders. Your home folder is `/home/ada`.
- `/etc`: the system's settings files.
- `/tmp`: temporary files (usually deleted when the computer restarts).
- `/usr` and `/bin`: programs. Commands like `ls` and `cat` are really small
  programs that live here.

These folders belong to the system; most of them you can only look at. You
do your own work in your home folder.

## What is a path?

A **path** is the directions to a file or folder. Folder names are joined
with `/`: `/home/ada/projects/site` means "start at the root, go into `home`,
then into `ada`, then `projects`, then `site`".

There are two kinds of paths:

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Absolute path</h4><p><code>/home/ada/projects/site</code></p><p>Starts with <code>/</code></p><p>Describes the way from the root</p><p>Points to the same place wherever you are</p></div>
    <div class="dim"><h4>Relative path</h4><p><code>projects/site</code></p><p>Does not start with <code>/</code></p><p>Starts from the folder you are in</p><p>Points somewhere else depending on where you are</p></div>
  </div>
  <figcaption>From your home folder both go to the same place. From <code>/tmp</code>, the relative path is looked up as <code>/tmp/projects/site</code>.</figcaption>
</figure>

- An **absolute path** starts with `/` and gives the directions from the
  root. Wherever you are, it always points to the same place.
- A **relative path** does not start with `/`; the directions start **from
  the folder you are in**. It is shorter, but it depends on where you are.

## Shortcuts: `~`, `.` and `..`

A few special signs appear inside paths:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>/</span><span>The root folder. At the start of a path it means "start from the root"; inside a path it separates folders.</span></div>
    <div class="anat-row"><span>~</span><span>Your home folder: <code>/home/ada</code>.</span></div>
    <div class="anat-row"><span>.</span><span>The folder you are in.</span></div>
    <div class="anat-row"><span>..</span><span>The folder above. <code>../..</code> is two above.</span></div>
    <div class="anat-row"><span>-</span><span>Only in <code>cd -</code>: the folder you were in before.</span></div>
  </div>
  <figcaption>The five signs used most often in paths.</figcaption>
</figure>

`..` goes up, `.` means "here". `~` is short for the absolute path of your
home folder; `~/projects` points to the `projects` folder in your home folder
from anywhere.

## Moving around with `cd`

`cd` (*change directory*) changes the folder you are in. You write a path
after it, relative or absolute:

```text
~ $ pwd
/home/ada
~ $ cd projects/site
~/projects/site $ pwd
/home/ada/projects/site
~/projects/site $ cd css
~/projects/site/css $ pwd
/home/ada/projects/site/css
~/projects/site/css $ cd ..
~/projects/site $ pwd
/home/ada/projects/site
~/projects/site $ cd ../..
~ $ pwd
/home/ada
~ $ cd /home/ada/projects/api
~/projects/api $ pwd
/home/ada/projects/api
~/projects/api $ cd
~ $ pwd
/home/ada
```

Notice:

- `cd projects/site` went down two levels at once; a path can contain as
  many folders as you like.
- `cd ..` went up one level, `cd ../..` two levels.
- `cd /home/ada/projects/api` was an absolute path; it would have gone there
  from anywhere.
- `cd` with nothing after it took you to your home folder. `cd ~` does the
  same.

The prompt changed at every step: the shell always shows you where you are.
If you are not sure, type `pwd`.

## Going back and forth: `cd -`

`cd -` takes you to **the previous** folder you were in and prints where you
arrived. It is very handy when you work between two folders:

```text
~ $ cd projects/site/css
~/projects/site/css $ cd -
/home/ada
~ $ cd -
/home/ada/projects/site/css
~/projects/site/css $ pwd
/home/ada/projects/site/css
```

## You do not have to go there to look

You can give `ls` a path too. To look inside a folder you do not need to go
into it:

```text
~ $ ls projects
api/  site/
~ $ ls projects/site
css/  index.html
~ $ ls ~/projects/api/docs
routes.txt
~ $ ls /etc
hostname  passwd  shells
~ $ ls .
notes/  projects/
~ $ ls ..
ada/
```

`ls ..` looked one level above the home folder, at `/home`: only `ada` is
there.

## A relative path depends on where you are

The same relative path points somewhere else from another folder. In `/tmp`
there is no `projects`:

```text
~ $ cd /tmp
/tmp $ ls projects
ls: cannot access 'projects': No such file or directory
/tmp $ ls ~/projects
api/  site/
/tmp $ cd projects
bash: cd: projects: No such file or directory
/tmp $ cd /home/ada/projects
~/projects $ pwd
/home/ada/projects
```

`~/projects` worked from anywhere, because `~` is short for an absolute path.
When you see an error saying "not here", the first question to ask is:
**where am I right now?**

## Errors

```text
~ $ cd nowhere
bash: cd: nowhere: No such file or directory
~ $ cd notes/todo.txt
bash: cd: notes/todo.txt: Not a directory
~ $ cd projects site
bash: cd: too many arguments
```

- `No such file or directory`: there is no folder with that name (or you are
  in the wrong place).
- `Not a directory`: what you gave is a file; `cd` only goes into folders.
- `too many arguments`: `cd` wants a single path, you gave two.

## Folders with spaces in their names

Because the shell splits the line at spaces, `cd my notes` gives `cd` two
separate arguments. You write a name that contains a space in **quotes**:

```text
~ $ mkdir "my notes"
~ $ ls
my notes/  notes/  projects/
~ $ cd my notes
bash: cd: too many arguments
~ $ cd "my notes"
~/my notes $ pwd
/home/ada/my notes
```

A real Linux terminal shows this name as `'my notes'` with quotes in the
`ls` output, to remind you that it contains a space. That is why many people
use `-` or `_` instead of spaces in file and folder names: `my-notes`,
`my_notes`.

## Windows paths and Git Bash

On Windows a path is written like `C:\Users\ada\Documents`: a drive letter at
the start and folders separated by **backslashes** (`\`). Git Bash shows the
same folder in the Linux style:

| Windows | Git Bash |
|---|---|
| `C:\Users\ada` | `/c/Users/ada` |
| `C:\Users\ada\Documents\notes.txt` | `/c/Users/ada/Documents/notes.txt` |
| `D:\photos` | `/d/photos` |

The drive letter looks like a folder under the root. On Linux and in Git Bash
folders are separated by **slashes** (`/`). One more difference: Windows
treats upper and lower case as the same, Linux does not; `Notes` and `notes`
are two different folders on Linux.

## Summary

- Linux has a single tree; its top is the root `/`, your place is `~`
  (`/home/ada`).
- An **absolute path** starts with `/` and points to the same place from
  anywhere; a **relative path** starts from the folder you are in.
- `.` is here, `..` is the folder above, `~` is your home folder.
- `cd path` to go, `cd ..` up, `cd` or `cd ~` home, `cd -` back.
- `ls path` looks inside without going there.
- Names with spaces are written in quotes.
