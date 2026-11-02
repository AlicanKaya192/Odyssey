# Creating Files and Folders

You can move around the file system now. Next comes creating your own folders
and files: setting up a folder skeleton for a project, creating empty files,
writing a few lines into a file and reading what you wrote. The commands of
this section are `mkdir`, `touch`, `echo` with `>`, `cat` and `rmdir`.

## Creating a folder: `mkdir`

`mkdir` (*make directory*) creates a new folder. If you give several names,
it creates all of them:

```text
~ $ mkdir blog
~ $ ls
blog/
~ $ mkdir blog/posts blog/images
~ $ ls blog
images/  posts/
~ $ mkdir blog
mkdir: cannot create directory 'blog': File exists
~ $ mkdir site/css
mkdir: cannot create directory 'site/css': No such file or directory
~ $ mkdir -p site/css
~ $ ls site
css/
~ $ mkdir -p site/css
```

Three things to notice:

1. When it succeeded it **printed nothing**. In the terminal silence usually
   means "done"; to be sure, you look with `ls`.
2. Trying to create an existing folder again gave `File exists`. It did not
   touch the old folder.
3. `mkdir site/css` failed because `site` did not exist yet: `mkdir` creates
   the **last** folder of the path and does not create the ones above it by
   itself.

For nested folders there is the `-p` (*parents*) option:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>mkdir site/css</h4><p>Fails if <code>site</code> does not exist</p><p>Creates only the last folder</p><p>If the folder exists: <code>File exists</code></p></div>
    <div class="ok"><h4>mkdir -p site/css</h4><p>Creates every missing folder</p><p><code>site</code>, then <code>css</code></p><p>Quietly does nothing if it exists</p></div>
  </div>
  <figcaption><code>-p</code> (parents): also create the folders above in the path if they are missing.</figcaption>
</figure>

Running the same command with `-p` a second time did not give an error
either. That is why scripts often use `mkdir -p`: the result is the same
whether the folder exists or not.

## Creating an empty file: `touch`

`touch` creates an **empty** file with the name you give:

```text
~/notes $ touch todo.txt
~/notes $ ls
todo.txt
~/notes $ cat todo.txt
~/notes $ touch a.txt b.txt c.txt
~/notes $ ls
a.txt  b.txt  c.txt  todo.txt
```

`cat todo.txt` printed nothing, because the file is empty. If the file
already exists, `touch` does not change its content; it only updates its
"last modified" time. That is where the name comes from: it touches the file
and moves on.

## Writing into a file: `echo` and `>`

The easiest way to create a file with text in it is `echo`. Normally `echo`
prints the text on the screen; if you add `> file` at the end, what it writes
goes to **the file** instead of the screen:

<figure class="fig">
  <pre><code class="language-text">echo "Buy milk" &gt; list.txt</code></pre>
  <div class="anat">
    <div class="anat-row"><span>echo</span><span>The command that writes the text.</span></div>
    <div class="anat-row"><span>"Buy milk"</span><span>The text to write.</span></div>
    <div class="anat-row"><span>&gt;</span><span>Send the output to a file instead of the screen. If the file does not exist it is created; if it does, it is <b>emptied</b> and written from the start.</span></div>
    <div class="anat-row"><span>&gt;&gt;</span><span>(instead of &gt;) <b>Add to the end</b> of the file; the old content stays.</span></div>
    <div class="anat-row"><span>list.txt</span><span>The file the output goes to.</span></div>
  </div>
  <figcaption>What the command would print flows into a file with <code>&gt;</code>. All the details of redirection come later in their own section.</figcaption>
</figure>

```text
~/notes $ echo "Buy milk" > list.txt
~/notes $ cat list.txt
Buy milk
~/notes $ echo "Call Ada" >> list.txt
~/notes $ cat list.txt
Buy milk
Call Ada
~/notes $ echo "Oops" > list.txt
~/notes $ cat list.txt
Oops
```

Look closely at the last two commands: `>` **erases** the file **without
asking** and writes it from the start. "Buy milk" and "Call Ada" are gone,
only "Oops" is left. When you want to add to the end of a file, always use
`>>`.

There is no text editor (nano, vim) in this terminal; you will write files
line by line with `echo`. On a real Linux this way is also used a lot for
short files and scripts.

## Reading a file: `cat`

`cat` prints the contents of a file. If you give several files, it prints
them one after the other; the name comes from the word *concatenate* (to join
one after another):

```text
~/notes $ cat shop.txt calls.txt
Buy milk
Call Ada
~/notes $ cat shop.txt nope.txt
Buy milk
cat: nope.txt: No such file or directory
~/notes $ cat -n shop.txt calls.txt
     1  Buy milk
     2  Call Ada
```

It printed an error for the file it could not find, but still printed the
other one. The `-n` option puts a number at the start of each line; the
numbers continued across the two files.

## Deleting an empty folder: `rmdir`

`rmdir` (*remove directory*) deletes a folder, but **only if it is empty**:

```text
~ $ mkdir empty
~ $ rmdir empty
~ $ ls
~ $ mkdir full
~ $ touch full/a.txt
~ $ rmdir full
rmdir: failed to remove 'full': Directory not empty
~ $ rmdir nope
rmdir: failed to remove 'nope': No such file or directory
```

`rmdir` does not delete a folder that has things in it; this is a safety
feature. The way to delete a folder together with its contents comes in the
next section (`rm -r`), explained separately because it is a command that
needs care.

## Hidden files

On Linux, to make a file or folder hidden you only need to start its name
with a **dot**. Being hidden only means that plain `ls` does not show it:

```text
~/notes $ touch .secret
~/notes $ ls
~/notes $ ls -a
./  ../  .secret
```

Programs often keep their settings in files like this: `.bashrc` in the home
folder holds bash's settings, `.gitignore` in a project is for Git.

## File names

```text
~/notes $ touch "my file.txt"
~/notes $ touch my-file.txt
~/notes $ touch Report.txt report.txt
~/notes $ ls
Report.txt  my file.txt  my-file.txt  report.txt
~/notes $ cat my file.txt
cat: my: No such file or directory
cat: file.txt: No such file or directory
```

This example shows three rules at once:

- A **space** separates arguments. `cat my file.txt` looked for two separate
  files. You write a file with a space in its name in quotes; but it is best
  to use `-` or `_` from the start.
- **Upper and lower case** are different: `Report.txt` and `report.txt` are
  two files. (`ls` listed the ones starting with a capital letter first.)
- The **extension** (`.txt`, `.md`) is part of the name. Linux does not
  decide what a file is from its extension; the extension is a hint for
  people and programs.

## Summary

- `mkdir a b` creates folders; for nested ones `mkdir -p a/b/c`.
- `touch file` creates an empty file and leaves an existing one alone.
- `echo "text" > file` writes the file from the start; `>>` adds to the end.
- `cat file` prints the contents; `cat -n` with line numbers.
- `rmdir folder` only deletes an empty folder.
- A file whose name starts with a dot is hidden; `ls -a` shows it.
- Use `-` or `_` instead of spaces in names; case matters.
