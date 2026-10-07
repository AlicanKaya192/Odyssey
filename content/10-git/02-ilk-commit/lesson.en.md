# The First Commit: Three Areas

Git is installed and knows your name. Now we can make the first commit. But
first we need to understand how Git looks at your files; that is the real
topic of this section. Half of Git's commands are about moving files between
the **three areas** described here.

## Three areas

<figure class="fig">
  <div class="flow">
    <span class="node">Working tree<br><small>files in the folder</small></span><span class="arrow">→</span>
    <span class="node acc">git add</span><span class="arrow">→</span>
    <span class="node">Staging area<br><small>the next commit</small></span><span class="arrow">→</span>
    <span class="node acc">git commit</span><span class="arrow">→</span>
    <span class="node ok">Repository<br><small>permanent history (.git)</small></span>
  </div>
  <figcaption>A change happens in the working tree first, moves to the staging area with git add, and into the repository with git commit.</figcaption>
</figure>

1. **Working tree**: how the files in the folder look right now. Everything
   you edit, delete or create happens here first. Git saves nothing here by
   itself.
2. **Staging area** (also called the *index*): where the changes that
   **will go into** the next commit are gathered. `git add` puts a change
   here.
3. **Repository**: where the commits, the permanent history, live (the
   `.git` folder). `git commit` writes what is in the staging area into it as
   one commit.

### Why is there a staging area in between?

Imagine you did three things one afternoon: added a heading to the home
page, fixed a typo on the contact page, and created a notes file for
yourself. Put them all in one commit and the answer to "what happened?" in
the history is muddled; and the notes file should never be committed at all.

The staging area lets you **choose what goes into a commit**: first you add
and commit the heading, then the typo fix; the notes file stays out. Each
commit tells one meaningful piece of work.

## An empty repository

In a new repository, `git status` says:

```text
~/site $ git init
Initialized empty Git repository in /home/ada/site/.git/
~/site (main) $ git status
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

`git status` is the most important command in Git. When you don't know what
to do, before and after a command: `git status`. Its output tells you the
state and also **what you can type next** (the `use "git add"…` lines in
brackets).

## Adding files: untracked files

Let's create two files:

```text
~/site (main) $ echo "<h1>Hello</h1>" > index.html
~/site (main) $ echo "body {}" > style.css
~/site (main) $ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html
        style.css

nothing added to commit but untracked files present (use "git add" to track)
```

Git sees the files but **does not track** them (*untracked*): they have never
been in Git's history. Git does not put them in commits unless you ask.

## `git add`: putting into the staging area

```text
~/site (main) $ git add index.html
~/site (main) $ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   index.html

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        style.css
```

`index.html` is now under **Changes to be committed**, in green, as
`new file`. `style.css` is still untracked because we didn't add it.

`git add` prints nothing when it succeeds. To see what happened:
`git status`.

| Command | Puts into the staging area |
|---|---|
| `git add index.html` | Only that file. |
| `git add index.html style.css` | The files you list. |
| `git add .` | All changes in the current folder (and below it). |
| `git add -A` | All changes in the whole repository, wherever you are. |

`git add .` is very handy, but careful: it can also add files you don't want
(a settings file with a password, a big data file). Look with `git status`
first to see what will be added. We will see how to keep unwanted files out
for good in section 05.

## `git commit`: taking the snapshot

```text
~/site (main) $ git commit -m "Add home page"
[main (root-commit) 5ab7f19] Add home page
 1 file changed, 1 insertion(+)
 create mode 100644 index.html
~/site (main) $ git status
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        style.css

nothing added to commit but untracked files present (use "git add" to track)
```

Let's read the output:

<figure class="fig">
  <pre><code class="language-text">[main (root-commit) 5ab7f19] Add home page
 1 file changed, 1 insertion(+)
 create mode 100644 index.html</code></pre>
  <div class="anat">
    <div class="anat-row"><span>main</span><span>The branch the commit was made on.</span></div>
    <div class="anat-row"><span>(root-commit)</span><span>The repository's first commit; nothing before it. Not shown on later commits.</span></div>
    <div class="anat-row"><span>5ab7f19</span><span>The short form of the commit's id (hash). Different for every commit.</span></div>
    <div class="anat-row"><span>Add home page</span><span>Your message.</span></div>
    <div class="anat-row"><span>1 file changed…</span><span>How many files changed, how many lines were added (+) or removed (-).</span></div>
    <div class="anat-row"><span>create mode 100644</span><span>A new file arrived; 100644 means an ordinary (non-executable) file.</span></div>
  </div>
  <figcaption>The output of the first commit. The id will differ in your terminal: the date and author go into it too.</figcaption>
</figure>

After the commit, `git status` no longer mentions `index.html`: the file is in
the commit and has not changed since. Only `style.css` is left.

> Without `-m`, `git commit` opens an editor for you to write the message.
> There is no editor in Odyssey's terminal; we will always write the message
> with `-m`.

### A good commit message

The message answers **why** for someone looking at the history (you, a few
months later). Three rules are enough for now:

- Keep it short (around 50 characters): `Add home page`.
- Start with an imperative verb: `Add`, `Fix`, `Remove`, `Update`. Like the
  answer to "what does this commit do if applied?".
- Avoid messages that say nothing, like `update`, `fix`, `asdf`.

More in section 15.

## Modified files

When you change a committed file, Git shows it as **modified**:

```text
~/site (main) $ echo "<p>Hi</p>" >> index.html
~/site (main) $ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   index.html

no changes added to commit (use "git add" and/or "git commit -a")
```

The red line says the change is not in the staging area yet (**Changes not
staged for commit**). To get it into a commit you need `git add` again. So
`git add` does not mean "add a new file" but "**put this change into the
next commit**"; a new file is also a change.

## The life cycle of a file

<figure class="fig">
  <div class="flow">
    <span class="node no">Untracked<br><small>new file</small></span><span class="arrow">→</span>
    <span class="node acc">Staged<br><small>git add</small></span><span class="arrow">→</span>
    <span class="node ok">Unmodified<br><small>git commit</small></span><span class="arrow">→</span>
    <span class="node no">Modified<br><small>edit the file</small></span><span class="arrow">→</span>
    <span class="node acc">Staged<br><small>git add</small></span>
  </div>
  <figcaption>A file cycles through these four states. After every edit it needs git add again to get into a commit.</figcaption>
</figure>

## Short status: `git status -s`

A two-letter summary instead of the long output:

```text
~/site (main) $ git status -s
M  about.html
 M index.html
MM style.css
?? notes.txt
```

| Code | Meaning |
|---|---|
| `??` | Untracked file. |
| `A ` | New file, in the staging area. |
| `M ` | Modified, in the staging area (left column, green). |
| ` M` | Modified, **not** in the staging area (right column, red). |
| `MM` | Partly staged, then modified again. |

The left column is the **staging area**, the right column the **working
tree**. `MM` is interesting: `git add` copies the change as it is at that
moment into the staging area. If you change the file again afterwards, the
new change stays outside; to get it into the commit you need `git add` again.

## Shortcut: `git commit -a`

`-a` (*all*) first stages every change in **tracked** files, then commits.
`-a` and `-m` combine into `-am`:

```text
~/site (main) $ git commit -am "Add greeting"
[main d00097d] Add greeting
 1 file changed, 1 insertion(+)
~/site (main) $ git status -s
?? todo.txt
```

Careful: `-a` **does not add new (untracked) files**. `todo.txt` stayed out.
New files always need `git add`.

## I added it by mistake: taking it out

If you put a new file into the staging area by mistake, `git status` tells
you what to do: `git rm --cached <file>`. The file stays in the folder; it
only leaves the staging area and becomes untracked again.

```text
~/site (main) $ git status -s
M  index.html
A  passwords.txt
~/site (main) $ git rm --cached passwords.txt
rm 'passwords.txt'
~/site (main) $ git status -s
M  index.html
?? passwords.txt
```

> `--cached` is essential. Without it, `git rm` **deletes the file from the
> folder too**. Taking a change to an already committed file out of the
> staging area works differently (`git restore --staged`); we will see it in
> section 04.

## Git does not track empty folders

Git tracks files, not folders. A folder with no files in it does not show up
in `git status` and does not go into commits. People who want to keep an
empty folder in a repository put an empty file named `.gitkeep` in it (a
convention; it means nothing special to Git).

## Summary

- Three areas: **working tree** → `git add` → **staging area** →
  `git commit` → **repository**.
- `git status` tells you everything; look before and after each step.
- `git add` puts a change into the next commit (a new file is a change too).
- `git commit -m "Message"` commits what is in the staging area.
- `git status -s`: the left column is the staging area, the right column the
  working tree.
- `git commit -am` is a shortcut for tracked files; it does not take new
  files.
- `git rm --cached` takes a new file out of the staging area without
  deleting it.
