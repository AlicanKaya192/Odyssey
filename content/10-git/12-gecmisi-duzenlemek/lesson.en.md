# Rewriting History

In 07 we saw how to merge branches: the work of two branches came together
with a merge commit. Git has a second way: **rebase**. In this section we
look at rebase, **cherry-pick**, which copies one commit to another branch,
and **interactive rebase**, which edits commits.

What they all have in common: **they create new commits and put them in place
of the old ones**. The hashes change. That's why the most important sentence
of this section is at the end: don't rewrite shared history.

## Rebase: moving your branch onto a new base

After you created the `feature` branch, `main` moved on. A merge (07) would
tie the two lines together with a merge commit. A rebase instead takes
`feature`'s commits and **replays them on the tip of `main`**: as if you had
created the branch today.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Before</span><span>Base → Add m (main) · Base → Add x → Add y (feature): the branches diverged.</span></div>
    <div class="anat-row"><span>git rebase main</span><span>feature's commits are reapplied one by one on the tip of main.</span></div>
    <div class="anat-row"><span>After</span><span>Base → Add m → Add x' → Add y' (feature): a straight line; x' and y' are new commits.</span></div>
  </div>
  <figcaption>A rebase changes where the branch starts (its base). Same content, new commits.</figcaption>
</figure>

```text
~/app (main) $ git log --oneline --graph --all
* 151c3bc (HEAD -> main) Add m
| * bf2c324 (feature) Add y
| * 3326390 Add x
|/  
* e3511dd Base
~/app (main) $ git switch feature
Switched to branch 'feature'
~/app (feature) $ git rebase main
Successfully rebased and updated refs/heads/feature.
~/app (feature) $ git log --oneline --graph --all
* 501f79f (HEAD -> feature) Add y
* 79c4ca6 Add x
* 151c3bc (main) Add m
* e3511dd Base
```

Before, the two branches had diverged; after the rebase, `feature` is a
straight line on top of `main`. `Add x` and `Add y` got new hashes (same
content, but their parents changed; remember the hash note in 03).

Now merging into `main` is a fast-forward; the history stays one straight
line:

```text
~/app (feature) $ git switch main
Switched to branch 'main'
~/app (main) $ git merge feature
Updating 151c3bc..501f79f
Fast-forward
 x.txt | 1 +
 y.txt | 1 +
 2 files changed, 2 insertions(+)
 create mode 100644 x.txt
 create mode 100644 y.txt
~/app (main) $ git log --oneline --graph
* 501f79f (HEAD -> main, feature) Add y
* 79c4ca6 Add x
* 151c3bc Add m
* e3511dd Base
```

## Merge or rebase?

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Merge</h4><p>History stays as it was</p><p>A merge commit is added</p><p>A fork and a join in the graph</p><p><b>Safe on shared branches</b></p></div>
    <div class="dim"><h4>Rebase</h4><p>Commits are rewritten</p><p>No merge commit</p><p>A straight line in the graph</p><p><b>Only for commits that are only yours</b></p></div>
  </div>
  <figcaption>Both bring two branches' work together; the difference is the shape of the history.</figcaption>
</figure>

Both produce the same files; the difference is the **shape** of the history.
Many teams do this: rebase to keep their own branch up to date (like
`git pull --rebase`), a PR merge to bring the branch into `main`.

## Conflicts during a rebase

A rebase applies the commits one by one; if one conflicts, it stops:

```text
~/app (feature) $ git rebase main
Auto-merging f.txt
CONFLICT (content): Merge conflict in f.txt
error: could not apply d6fe9d2... Double a
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
Could not apply d6fe9d2... # Double a
~/app (feature|REBASE) $ git status
interactive rebase in progress; onto 6b9e1d8
Last command done (1 command done):
   pick d6fe9d2 # Double a
No commands remaining.
You are currently rebasing branch 'feature' on '6b9e1d8'.
  (fix conflicts and then run "git rebase --continue")
  (use "git rebase --skip" to skip this patch)
  (use "git rebase --abort" to check out the original branch)

Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)
        both modified:   f.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

The prompt became `(feature|REBASE)`; HEAD is detached because while
replaying commits Git isn't on any branch. Resolving is like a merge, but to
finish you use `--continue` instead of commit:

1. Fix the file, delete the markers.
2. `git add file`
3. `git rebase --continue` (moves on to the next commits)

```text
~/app (feature|REBASE) $ cat f.txt
<<<<<<< HEAD
A
=======
aa
>>>>>>> d6fe9d2 (Double a)
~/app (feature|REBASE) $ echo "AA" > f.txt
~/app (feature|REBASE) $ git add f.txt
~/app (feature|REBASE) $ git rebase --continue
[detached HEAD 3c1e0ed] Double a
 1 file changed, 1 insertion(+), 1 deletion(-)
Successfully rebased and updated refs/heads/feature.
~/app (feature) $ git log --oneline --graph
* 3c1e0ed (HEAD -> feature) Double a
* 6b9e1d8 (main) Upper a
* e3511dd Base
```

| Command | What it does |
|---|---|
| `git rebase --continue` | Applies the resolved commit and continues. |
| `git rebase --skip` | Skips this commit and continues (its change is lost). |
| `git rebase --abort` | Puts everything back to before the rebase. |

> In a rebase `ours` / `theirs` **swap**: `ours` is the base being built on
> (`main`), `theirs` is your commit being applied. That's where the confusion
> comes from; editing by hand is safer.

## `git pull --rebase`

In 09, `git pull --no-rebase` created a merge commit for diverged branches.
`--rebase` instead replays your local commits **on top of** the ones from
GitHub; no merge commit:

```text
~/app (main) $ git pull --rebase
From https://github.com/ada/app
   e3511dd..bb21734  main       -> origin/main
Successfully rebased and updated refs/heads/main.
~/app (main) $ git log --oneline --graph
* ec2ffa2 (HEAD -> main) Add x
* bb21734 (origin/main, origin/HEAD) Add g
* e3511dd Base
~/app (main) $ git push
To https://github.com/ada/app.git
   bb21734..ec2ffa2  main -> main
```

To avoid typing it every time: `git config --global pull.rebase true`.

## Cherry-pick: taking a single commit

Sometimes you don't need a whole branch, only **one commit** of it: a bug
fixed on another branch that `main` needs too. `git cherry-pick <commit>`
applies that commit's change to the branch you are on as **a new commit**.

```text
~/app (main) $ git log --oneline experiment
d9f2c85 (experiment) Try flex layout
57015e0 Fix footer typo
5a6c6f0 Try grid layout
c9193f2 (HEAD -> main) Add footer
e3511dd Base
~/app (main) $ git cherry-pick experiment~1
[main 79b28fa] Fix footer typo
 Date: Wed Oct 7 10:03:00 2026 +0300
 1 file changed, 1 insertion(+), 1 deletion(-)
~/app (main) $ git log --oneline -3
79b28fa (HEAD -> main) Fix footer typo
c9193f2 Add footer
e3511dd Base
~/app (main) $ cat footer.html
<footer>Copyright</footer>
~/app (main) $ ls
f.txt  footer.html
```

Same message and change, different hash (different parent). If there's a
conflict the fix is the same: resolve, `git add`, `git cherry-pick
--continue` (or `--abort`).

## Interactive rebase: editing commits

`git rebase -i HEAD~3` opens the last three commits as a list in an editor.
You say what to do by changing the word at the start of each line:

```text
pick 1a2b3c4 Add search box
squash 5d6e7f8 wip
reword 9a8b7c6 Fix serch
```

| Word | What it does |
|---|---|
| `pick` | Keep the commit as it is. |
| `reword` | Change its message. |
| `squash` | Combine it with the previous one (messages too). |
| `fixup` | Combine it with the previous one, drop its own message. |
| `drop` | Delete the commit. |
| order of the lines | Changes the order of the commits. |

When you save and close, Git applies the list. This is the most common way
to clean up `wip`, `fix`, `typo` commits before opening a PR.

> Since Odyssey's terminal has no editor, interactive rebase doesn't work in
> it; you reach some of the same results in other ways: combining the last
> commits with `git reset --soft` + commit (04), changing the last message
> with `--amend`.

## The golden rule

**Don't rebase commits others have already received** (nor change them with
`--amend` or `reset`). A rebase creates new commits; the old ones stay on
other people's computers. If you force-push the new history (09), their
history and yours split apart and work can be lost.

Safe use: commits that **are only yours** (not pushed yet, or a branch only
you work on).

## Summary

- `git rebase main`: replays your branch's commits on the tip of `main`; the
  history stays straight, the hashes change.
- On a conflict: fix → `git add` → `git rebase --continue` (or `--abort`,
  `--skip`).
- `git pull --rebase` replays local commits on top of the incoming ones.
- `git cherry-pick <commit>` copies a single commit to your branch.
- `git rebase -i` combines, renames and deletes commits (in a real
  terminal).
- Don't rewrite shared history.
