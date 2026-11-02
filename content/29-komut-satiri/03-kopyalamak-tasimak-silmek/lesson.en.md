# Copying, Moving, Deleting

In a graphical interface you right-click to copy a file, drag it to move it
and throw it in the recycle bin to delete it. In the terminal these three
jobs are three commands: `cp`, `mv` and `rm`. All three are short and fast;
`rm`, however, **cannot be undone**, so part of this section is about ways
to be careful.

## Two commands, one difference

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>cp source target</h4><p>The source stays where it is</p><p>A copy appears at the target</p><p>Folders need <code>-r</code></p></div>
    <div class="dim"><h4>mv source target</h4><p>The source leaves its place</p><p>It becomes the target (a move or a new name)</p><p>Folders need no option</p></div>
  </div>
  <figcaption>For both: if the target is an existing folder, the file goes <b>into</b> it; otherwise the target is the new name.</figcaption>
</figure>

Both are written the same way: first the **source**, the **target** last.

```text
cp  source  target
mv  source  target
```

## Copying: `cp`

`cp` (*copy*) creates a copy of the source at the target:

```text
~/notes $ cp todo.txt todo-copy.txt
~/notes $ ls
ideas.txt  todo-copy.txt  todo.txt
~/notes $ cat todo-copy.txt
Buy milk
~/notes $ mkdir backup
~/notes $ cp todo.txt backup/
~/notes $ cp todo.txt ideas.txt backup
~/notes $ ls backup
ideas.txt  todo.txt
~/notes $ cp nope.txt backup
cp: cannot stat 'nope.txt': No such file or directory
```

- `cp todo.txt todo-copy.txt` created a second file in the same folder.
- `cp todo.txt backup/` copied the file **into** the `backup` folder; the
  name stayed the same.
- You can give several sources; then the last argument must be a folder.
- Trying to copy a file that does not exist gave `cannot stat`: "I could not
  look at that file's details, because it is not there".

What the target means is always decided by one question: **is the target an
existing folder?**

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>cp a.txt b.txt</span><span>If <code>b.txt</code> does not exist: a copy of a.txt named b.txt. If it does: <b>overwritten without asking</b>.</span></div>
    <div class="anat-row"><span>cp a.txt backup/</span><span><code>backup</code> is a folder: the copy becomes <code>backup/a.txt</code>.</span></div>
    <div class="anat-row"><span>cp a.txt b.txt backup/</span><span>Several sources: the last argument must be a folder.</span></div>
    <div class="anat-row"><span>mv old.txt new.txt</span><span>A new name in the same folder: renaming.</span></div>
    <div class="anat-row"><span>mv a.txt archive/</span><span>A move into the folder; the name stays the same.</span></div>
  </div>
  <figcaption>The last argument is always the target. Whether the target is an existing folder decides what happens.</figcaption>
</figure>

## Copying a folder: `cp -r`

`cp` does not copy a folder on its own. To copy it with everything inside, it
needs the `-r` option (*recursive*: all the way down, every level):

```text
~/notes $ cp site site-backup
cp: -r not specified; omitting directory 'site'
~/notes $ cp -r site site-backup
~/notes $ ls site-backup
index.html
~/notes $ cp -r site site-backup
~/notes $ ls site-backup
index.html  site/
```

Look at the last two commands: because `site-backup` now exists, the second
`cp -r site site-backup` copied `site` **into** it. Running the same command
twice does not give the same result twice; the state of the target at that
moment matters.

## Overwriting is not asked about

If there is already a file with the same name at the target, `cp` (and `mv`)
writes over it **without asking**:

```text
~/notes $ cat ideas.txt
Ideas
~/notes $ cp todo.txt ideas.txt
~/notes $ cat ideas.txt
Buy milk
```

The old content of `ideas.txt` is gone. That is why backing up an important
file before changing it is a good habit: `cp notes.txt notes.txt.bak`.

## Moving and renaming: `mv`

`mv` (*move*) moves a file or folder somewhere else. If you give it a new name
in the same folder, you have **renamed** it; Linux has no separate "rename"
command:

```text
~/notes $ mv todo.txt shopping.txt
~/notes $ ls
ideas.txt  shopping.txt
~/notes $ mkdir archive
~/notes $ mv shopping.txt archive/
~/notes $ ls
archive/  ideas.txt
~/notes $ ls archive
shopping.txt
~/notes $ mv archive old-notes
~/notes $ ls
ideas.txt  old-notes/
~/notes $ mv nope.txt archive
mv: cannot stat 'nope.txt': No such file or directory
```

- `mv todo.txt shopping.txt` only changed the name.
- `mv shopping.txt archive/` moved the file into the folder.
- `mv archive old-notes` renamed a **folder**. Unlike `cp`, `mv` needs no
  option for folders; the contents come along as they are.

## Deleting: `rm`

`rm` (*remove*) deletes files. To delete a folder with everything inside, it
again needs `-r`:

```text
~/notes $ ls
ideas.txt  old.txt  tmp/  todo.txt
~/notes $ rm old.txt
~/notes $ rm tmp
rm: cannot remove 'tmp': Is a directory
~/notes $ rm -r tmp
~/notes $ ls
ideas.txt  todo.txt
~/notes $ rm nope.txt
rm: cannot remove 'nope.txt': No such file or directory
~/notes $ rm -f nope.txt
```

- `rm tmp` refused to delete the folder (`Is a directory`); `rm -r tmp`
  deleted it.
- `rm -f` (*force*) did not complain about the missing file. `-f` asks
  nothing and objects to nothing; that is why it is dangerous.

> **`rm` cannot be undone.** There is no recycle bin in the terminal; a
> deleted file is gone. Especially before typing `rm -rf` (with contents,
> without asking), read the path twice.

## If you want it to ask: `rm -i`

The `-i` (*interactive*) option asks before deleting each file. In a real
terminal it looks like this; if you type `y` it deletes, anything else leaves
the file alone:

```text
$ rm -i todo.txt
rm: remove regular file 'todo.txt'? n
```

Odyssey's terminal cannot take an answer from the keyboard, so `rm -i` deletes
nothing here and only prints a message saying so. Still, remember it as a
habit: for deletions you are not sure about, `-i` is a good seat belt.

## Summary

- `cp source target` copies, the source stays; for a folder `cp -r`.
- `mv source target` moves or renames; it works on folders too.
- If the target is an existing folder, the file goes into it; with several
  sources the last argument must be a folder.
- `cp` and `mv` overwrite an existing file without asking.
- `rm file` deletes, `rm -r folder` deletes with contents, `-f` never asks.
- `rm` cannot be undone: look with `ls` first, back up important files.
