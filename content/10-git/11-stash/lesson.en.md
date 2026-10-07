# Stash: Putting Work Aside

You are in the middle of half-done work on a branch. Right then an urgent
request comes in: a typo on `main` must be fixed now. You need to switch
branches, but:

- You don't want to commit the half-done work (it doesn't work yet; it would
  pollute the history).
- If you try to switch without committing, Git either carries the change
  along or refuses (06).

**Stash** is made exactly for this: it puts your uncommitted changes aside and
cleans the working tree. When you're done, you bring them back.

<figure class="fig">
  <div class="flow">
    <span class="node no">Half-done work<br><small>uncommitted</small></span><span class="arrow">→</span>
    <span class="node acc">git stash</span><span class="arrow">→</span>
    <span class="node ok">Clean tree<br><small>other work</small></span><span class="arrow">→</span>
    <span class="node acc">git stash pop</span><span class="arrow">→</span>
    <span class="node no">It's back</span>
  </div>
  <figcaption>A stash puts uncommitted changes aside; when you bring them back you continue where you left off.</figcaption>
</figure>

## Putting aside and bringing back

```text
~/site (main) $ echo "h1 {color: red}" >> style.css
~/site (main) $ git status -s
 M style.css
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (5e414f930ae1a4280290b7040f79f5b9c495f800)
```

- `git stash` put the changes away; `git status` is clean. Now you can switch
  branches freely.
- `Saved working directory and index state WIP on main: …` means "the work in
  progress on top of this commit of main was saved".
- `git stash pop` brings back the latest one and removes it from the list.

## The urgent job scenario

```text
~/site (redesign) $ echo "h1 {font-size: 3em}" >> style.css
~/site (redesign) $ git stash
Saved working directory and index state WIP on redesign: e20491f Add home page
~/site (redesign) $ git switch main
Switched to branch 'main'
~/site (main) $ echo "<h1>Welcome</h1>" > index.html
~/site (main) $ git commit -am "Fix typo"
[main baff07e] Fix typo
 1 file changed, 1 insertion(+), 1 deletion(-)
~/site (main) $ git switch redesign
Switched to branch 'redesign'
~/site (redesign) $ git stash pop
On branch redesign
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (ee4d503a89591f06c196b2b1fc1bccbc64a59df2)
```

The half-done work was never committed, the urgent fix was made on its own
branch and is ready to push, and then you continued where you left off.

## Several stashes

The stash is a **stack**: every `git stash` puts a new entry on top. `git
stash list` shows them all; the newest is `stash@{0}`, the one before it
`stash@{1}`. A message makes them easier to find:

```text
~/site (main) $ echo "h1 {color: red}" >> style.css
~/site (main) $ git stash push -m "try red"
Saved working directory and index state On main: try red
~/site (main) $ echo "h1 {color: blue}" >> style.css
~/site (main) $ git stash push -m "try blue"
Saved working directory and index state On main: try blue
~/site (main) $ git stash list
stash@{0}: On main: try blue
stash@{1}: On main: try red
~/site (main) $ git stash show stash@{1}
 style.css | 1 +
 1 file changed, 1 insertion(+)
~/site (main) $ git stash apply stash@{1}
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

no changes added to commit (use "git add" and/or "git commit -a")
~/site (main) $ git stash list
stash@{0}: On main: try blue
stash@{1}: On main: try red
```

| Command | What it does |
|---|---|
| `git stash` | Puts the changes away (message: `WIP on branch: …`). |
| `git stash push -m "message"` | Puts them away with your own message. |
| `git stash list` | Lists the entries. |
| `git stash show` | Shows which files the latest one changed; `-p` for the diff. |
| `git stash pop` | Applies the latest one and **removes** it. |
| `git stash apply stash@{1}` | Applies a given entry, **doesn't remove** it. |
| `git stash drop stash@{1}` | Removes an entry without applying it. |
| `git stash clear` | ⚠ Removes all entries. |

The difference between `pop` and `apply`: `apply` keeps the entry in the list;
useful if you want to apply the same change to another branch as well.

## Untracked files: `-u`

By default `git stash` only takes changes in **tracked** files. A new
(untracked) file stays in the folder:

```text
~/site (main) $ echo "h1 {}" >> style.css
~/site (main) $ echo "draft" > notes.txt
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
?? notes.txt
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (cb05b8cf2da6315c557d413607b2148bcd53da62)
~/site (main) $ git stash -u
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git status -s
~/site (main) $ git stash pop
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   style.css

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (be19b371c1deda113dd29deeefbaf38b9d5cf94b)
```

`-u` (*include untracked*) puts new files away too.

## Bringing it back on another branch

A stash isn't tied to a branch. If you notice you started working on the
wrong branch: stash, switch to the right branch, bring it back there.

```text
~/site (main) $ echo "<input>" >> index.html
~/site (main) $ git stash
Saved working directory and index state WIP on main: e20491f Add home page
~/site (main) $ git switch -c search
Switched to a new branch 'search'
~/site (search) $ git stash pop
On branch search
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   index.html

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (42a7a3946d54809cbde91659c0d836f0e285e9c7)
~/site (search) $ git commit -am "Add search box"
[search 623d81e] Add search box
 1 file changed, 1 insertion(+)
~/site (search) $ git log --oneline --all
623d81e (HEAD -> search) Add search box
e20491f (main) Add home page
```

## Conflicts

When bringing a stash back, if the same lines changed in the meantime there
can be a conflict, as in a merge. The fix is the same: fix the file, `git
add`. If there is a conflict, `pop` does **not** remove the entry (so no work
is lost); after resolving, you remove it with `git stash drop`.

## Stash or commit?

A stash is a short-term pocket: minutes or hours. Work left for days gets
forgotten in the stash; the list grows and you lose track of what's what.
For work that has to wait long, open a branch and commit (the message can be
`WIP`; fix it later with `--amend` or a squash).

## Summary

- `git stash` puts uncommitted changes away and cleans the working tree;
  `git stash pop` brings them back.
- The stash is a stack: `stash@{0}` is the newest; `list`, `show`, `apply`,
  `drop`.
- `-m` for a message, `-u` for untracked files.
- A stash isn't tied to a branch; it can be brought back on another branch.
- Stash for the short term, branch + commit for the long term.
