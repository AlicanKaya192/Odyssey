# Merging

You worked on a branch, the work is done and you like it. Now you want to
bring that work into the main branch (`main`). That is called **merging**:
adding one branch's commits to another branch.

## How?

Two steps; the order matters:

1. Switch to the branch that **receives** the change: `git switch main`.
2. Name the branch to bring in: `git merge about`.

Read it as "merge about into main". The command changes the branch you are
on and leaves the named branch alone.

Git merges in two different ways; the shape of the history decides which.

## 1. Fast-forward

If no commit was made on `main` after the `about` branch was created, it is
easy: `main`'s label is **slid** to `about`'s last commit. No new commit is
made.

<figure class="fig">
  <div class="flow">
    <span class="node">Add home page<br><small>main (before)</small></span><span class="arrow">→</span>
    <span class="node acc">Add about page<br><small>about, main (after)</small></span>
  </div>
  <figcaption>main was still where the branch split off; merging only slid the main label to about's commit.</figcaption>
</figure>

```text
~/site (main) $ git log --oneline --graph --all
* 14643f4 (about) Add about page
* a0cf655 (HEAD -> main) Add home page
~/site (main) $ git merge about
Updating a0cf655..14643f4
Fast-forward
 about.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 about.html
~/site (main) $ git log --oneline --graph --all
* 14643f4 (HEAD -> main, about) Add about page
* a0cf655 Add home page
```

The `Fast-forward` in the output says so. The history stayed a straight
line.

## 2. Three-way merge and the merge commit

If commits were also made on `main` while you worked on `contact`, the two
branches have **diverged**; sliding the label would lose the work on `main`.
In this case Git looks at three things: the last commits of the two branches
and the **common ancestor** where they split (the *merge base*). Then it
creates a new commit combining both sets of changes: a **merge commit**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Common ancestor</span><span>Add home page — the two branches split here.</span></div>
    <div class="anat-row"><span>Tip of main</span><span>Add styles — a commit made on main afterwards.</span></div>
    <div class="anat-row"><span>Tip of contact</span><span>Add contact page — the commit made on the branch.</span></div>
    <div class="anat-row"><span>Merge commit</span><span>Merge branch 'contact' — has two parents, carries both sets of changes.</span></div>
  </div>
  <figcaption>A three-way merge: Git looks at what changed on each branch since the common ancestor and combines both.</figcaption>
</figure>

```text
~/site (main) $ git log --oneline --graph --all
* 23a2dc6 (HEAD -> main) Add styles
| * de0737c (contact) Add contact page
|/  
* a0cf655 Add home page
~/site (main) $ git merge contact --no-edit
Merge made by the 'ort' strategy.
 contact.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (main) $ git log --oneline --graph
*   247f509 (HEAD -> main) Merge branch 'contact'
|\  
| * de0737c (contact) Add contact page
* | 23a2dc6 Add styles
|/  
* a0cf655 Add home page
```

The merge commit has **two parents**: `main`'s previous last commit and
`contact`'s last commit. The `|\` and `|/` in the graph show where the branch
split off and joined back.

> **In a real terminal**, for a three-way merge Git opens an editor so you
> can edit the commit message; the ready-made message (`Merge branch
> 'contact'`) is usually enough, so you save and close. To skip the editor,
> use `--no-edit` (ready-made message) or `-m "message"`. There is no editor
> in Odyssey's terminal; we will use `--no-edit` or `-m`.

## Always a merge commit: `--no-ff`

If you want a merge commit even when a fast-forward is possible, use
`--no-ff` (*no fast-forward*). Some teams like this: the graph keeps the
information "these commits were made on a branch and merged at this point".

```text
~/site (main) $ git merge --no-ff about --no-edit
Merge made by the 'ort' strategy.
 about.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 about.html
~/site (main) $ git log --oneline --graph
*   8fbaac5 (HEAD -> main) Merge branch 'about'
|\  
| * 14643f4 (about) Add about page
|/  
* a0cf655 Add home page
```

## Already merged

If you try to merge the same branch twice, Git finds nothing to do:

```text
~/site (main) $ git merge contact
Already up to date.
```

## Keeping your branch up to date

While you work on a long-running branch, `main` moves on. If your branch
falls far behind, merging at the end gets harder. The fix is to **merge
`main` into your branch** now and then: the same command, the other way
round.

```text
~/site (main) $ git switch feature
Switched to branch 'feature'
~/site (feature) $ git merge main --no-edit
Merge made by the 'ort' strategy.
 news.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 news.txt
~/site (feature) $ git log --oneline --graph
*   82518df (HEAD -> feature) Merge branch 'main'
|\  
| * 5df455c (main) Add news
* | c62bac9 Start feature
|/  
* a0cf655 Add home page
~/site (feature) $ ls
feature.txt  index.html  news.txt
```

Now the `feature` branch also contains what's new on `main`; you continue
your work on top of it.

## After merging

Merging does not delete the branch. Cleaning up finished branches is a good
habit:

```text
~/site (main) $ git branch --merged
  about
  contact
* main
~/site (main) $ git branch -d about contact
Deleted branch about (was 14643f4).
Deleted branch contact (was d1d3ccd).
~/site (main) $ git branch
* main
  wip
```

`git branch -d` deletes merged branches without complaint (the `--merged`
list shows those that are safe to delete). The branch's commits aren't lost:
they now live in `main`'s history.

## What if both branches changed the same line?

In most cases Git combines the two branches' changes by itself: different
files, or different places in the same file. But if both branches changed
**the same line differently**, it can't know which is right and asks you:
that is a **conflict**. The topic of the next section.

## Summary

- Merging: switch to the branch that receives the change, `git merge
  <branch>`.
- If the target branch hasn't moved, a **fast-forward**: the label slides,
  no new commit.
- If the branches diverged, a **three-way merge**: a merge commit with two
  parents is created.
- `--no-edit` uses the ready-made message, `-m` gives your own, `--no-ff`
  always creates a merge commit.
- To update your branch, merge `main` into it.
- Merging doesn't delete the branch; clean up with `git branch -d`.
