# Seeing Changes

One of Git's biggest benefits is **looking back**: what did you change,
what haven't you committed yet, what did this file look like three days ago,
who wrote this line? In this section we learn how to ask Git questions. None
of these commands change anything; they only **show**. So try them freely.

All the examples in this section use the same small repository: a to-do
list (`todo.txt`) and a `readme.md` in the `notes` folder, three commits.

```text
~/notes (main) $ git log --oneline
f2dfe4a (HEAD -> main) Add readme
ed15a33 Add call
20c376c Add todo list
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

## `git diff`: changes not staged yet

`git status` tells you which file changed, not **what** changed. `git diff`
shows that:

```text
~/notes (main) $ echo "Buy bread" >> todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git diff
diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread
```

The output looks busy at first; let's read it piece by piece:

<figure class="fig">
  <pre><code class="language-text">diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread</code></pre>
  <div class="anat">
    <div class="anat-row"><span>diff --git a/… b/…</span><span>Which file's diff. a/ is the old version, b/ the new one.</span></div>
    <div class="anat-row"><span>index ab0af58..254c209</span><span>Short ids of the old and new content. You can skip it when reading.</span></div>
    <div class="anat-row"><span>--- / +++</span><span>Lines marked minus come from the old file, lines marked plus from the new one.</span></div>
    <div class="anat-row"><span>@@ -1,2 +1,3 @@</span><span>Where the hunk is: 2 lines from line 1 in the old file, 3 lines from line 1 in the new.</span></div>
    <div class="anat-row"><span>(space) Buy milk</span><span>An unchanged line, there to show where the change is.</span></div>
    <div class="anat-row"><span>+Buy bread</span><span>An added line (green). A removed line starts with - (red).</span></div>
  </div>
  <figcaption>The parts of a diff. The last lines are what matter: + added, - removed.</figcaption>
</figure>

In short: **a line starting with `+` was added, a line starting with `-`
was removed**, a line starting with a space did not change (it is there to
show the position). To Git, changing a line means "remove the old one, add
the new one":

```text
~/notes (main) $ echo "Buy oat milk" > todo.txt
~/notes (main) $ echo "Call Ada" >> todo.txt
~/notes (main) $ git diff
diff --git a/todo.txt b/todo.txt
index ab0af58..76b6afb 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,2 @@
-Buy milk
+Buy oat milk
 Call Ada
```

## Which diff compares what?

`git diff` on its own compares **the working tree with the staging area**.
That is why it looks empty after `git add`: the change is now the same on
both sides. To see a staged change you need `--staged`:

```text
~/notes (main) $ git add todo.txt
~/notes (main) $ git diff
~/notes (main) $ git diff --staged
diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread
```

<figure class="fig">
  <div class="flow">
    <span class="node">Working tree</span><span class="arrow">↔</span>
    <span class="node acc">git diff</span><span class="arrow">↔</span>
    <span class="node">Staging area</span><span class="arrow">↔</span>
    <span class="node acc">git diff --staged</span><span class="arrow">↔</span>
    <span class="node ok">Last commit</span>
  </div>
  <figcaption>git diff compares the first two, git diff --staged the last two. git diff HEAD compares the working tree directly with the last commit.</figcaption>
</figure>

`--staged` and `--cached` are the same thing; you will see both. Typing
`git diff --staged` before committing is a good habit: it shows **exactly
what** goes into the commit.

If you want a summary instead of details:

| Command | Shows |
|---|---|
| `git diff --stat` | How many lines changed per file. |
| `git diff --name-only` | Only the names of the changed files. |
| `git diff readme.md` | Only the diff of that file. |

## `git log`: the history

```text
~/notes (main) $ git log
commit f2dfe4a515f091cc7d1464d0a4aa58e0e52e1f08 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Add readme

commit ed15a3351e08dfbd752a5e9479e4fe56643b06e3
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Add call

commit 20c376c07d02ed31d1fcfbd46189e96dac4cc468
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:00:00 2026 +0300

    Add todo list
```

For each commit: the id (*hash*), author, date and message. Newest at the
top.

The **hash** is a 40-character string of letters and digits; it is computed
from the commit's content, so it is different for every commit. You don't
need all of it: the first 7 characters (`ed15a33`) are enough for Git, and
`--oneline` shows exactly those.

> In a real terminal, when `git log` is long the output opens in a pager; you
> see `:` on the bottom line. Space moves on, **`q`** quits.

### Common options

| Command | Shows |
|---|---|
| `git log --oneline` | One line per commit: short hash + message. |
| `git log -n 3` or `git log -3` | Only the last 3 commits. |
| `git log --stat` | Which files changed in each commit, and by how many lines. |
| `git log -p` | The full diff (*patch*) of each commit. |
| `git log -- todo.txt` | Only the commits that changed this file. |
| `git log --author=Ada` | Only those whose author contains "Ada". |
| `git log --grep=fix -i` | Those whose message contains "fix"; `-i` ignores case. |
| `git log --reverse` | Oldest to newest. |

Options combine: `git log --oneline --author=Grace -- todo.txt`.

Say a friend, Grace, also made two commits in the repository:

```text
~/notes (main) $ git log --oneline
f0413ac (HEAD -> main) Mention Grace
c0237ac Add garden tasks
f2dfe4a Add readme
ed15a33 Add call
20c376c Add todo list
~/notes (main) $ git log --oneline --author=Grace
f0413ac (HEAD -> main) Mention Grace
c0237ac Add garden tasks
~/notes (main) $ git log --oneline -- readme.md
f0413ac (HEAD -> main) Mention Grace
f2dfe4a Add readme
~/notes (main) $ git log --oneline -i --grep=grace
f0413ac (HEAD -> main) Mention Grace
```

You can also print lines in your own layout: in `--format`, `%h` is the
short hash, `%an` the author, `%ad` the date, `%s` the message.

```text
~/notes (main) $ git log --format="%h %an: %s"
f0413ac Grace Hopper: Mention Grace
c0237ac Grace Hopper: Add garden tasks
f2dfe4a Ada Lovelace: Add readme
ed15a33 Ada Lovelace: Add call
20c376c Ada Lovelace: Add todo list
```

## HEAD and counting back

You don't have to name every commit by its hash. **HEAD** means "the commit
you are on right now" (usually the last commit of your branch). You count
back from it with `~`:

<figure class="fig">
  <div class="flow">
    <span class="node">Add todo list<br><small>HEAD~2</small></span><span class="arrow">→</span>
    <span class="node">Add call<br><small>HEAD~1</small></span><span class="arrow">→</span>
    <span class="node acc">Add readme<br><small>HEAD (main)</small></span>
  </div>
  <figcaption>HEAD is the commit you are on; HEAD~1 the one before, HEAD~2 two before. A branch name (main) also means that branch's last commit.</figcaption>
</figure>

These names can be used instead of a hash in any command.

## `git show`: a single commit

`git show` shows a commit's information and its diff together. Without a
name, it shows HEAD:

```text
~/notes (main) $ git show
commit f2dfe4a515f091cc7d1464d0a4aa58e0e52e1f08 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Add readme

diff --git a/readme.md b/readme.md
new file mode 100644
index 0000000..17e0f0d
--- /dev/null
+++ b/readme.md
@@ -0,0 +1 @@
+# Notes
```

Two very handy forms:

- `git show --stat HEAD~1`: which files changed in that commit.
- `git show HEAD~2:todo.txt`: the file **as it was in that commit**. It does
  not change the file, it only prints it.

```text
~/notes (main) $ git show --stat HEAD~1
commit ed15a3351e08dfbd752a5e9479e4fe56643b06e3
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Add call

 todo.txt | 1 +
 1 file changed, 1 insertion(+)
~/notes (main) $ git show HEAD~2:todo.txt
Buy milk
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

## Comparing two commits

`git diff` can also take two commits: "what changed from then to now?"

```text
~/notes (main) $ git diff HEAD~2 HEAD --stat
 readme.md | 1 +
 todo.txt  | 1 +
 2 files changed, 2 insertions(+)
~/notes (main) $ git diff HEAD~2 HEAD -- todo.txt
diff --git a/todo.txt b/todo.txt
index dea7672..ab0af58 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1 +1,2 @@
 Buy milk
+Call Ada
```

## `git blame`: who wrote this line?

`git blame file` writes next to each line the commit that changed it **last**,
with the author and date:

```text
~/notes (main) $ git blame todo.txt
^20c376c (Ada Lovelace 2026-10-07 10:00:00 +0300 1) Buy milk
ed15a335 (Ada Lovelace 2026-10-07 10:01:00 +0300 2) Call Ada
c0237aca (Grace Hopper 2026-10-07 10:03:00 +0300 3) Water the plants
```

A hash starting with `^` is the repository's first commit. Despite the name,
its real use is finding **why** a line is the way it is: take the hash and
read that commit's message with `git show`.

## Summary

- `git diff`: working tree ↔ staging area (what you haven't added yet).
- `git diff --staged`: staging area ↔ last commit (what goes into the
  commit).
- `git diff A B`: between two commits.
- `git log` shows the history; filter it with `--oneline`, `-n`, `--stat`,
  `-p`, `--author`, `--grep`, `-- file`.
- `HEAD` is the commit you are on; `HEAD~1` the one before, `HEAD~2` two
  before.
- `git show` shows a commit, `git show REV:file` a file as it was then.
- `git blame` tells you the commit where each line last changed.
