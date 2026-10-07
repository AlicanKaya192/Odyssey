# Undoing Things

The real reason to use Git: **not being afraid of mistakes**. You deleted the
wrong file, committed with a file missing, a change broke everything... There
is a way back from each. In this section we see which command fits which
situation.

First an important warning: some undo commands **permanently delete
uncommitted** work. Git can only protect what has been committed. Those
commands are marked with ⚠.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>In the file (not added yet)</span><span>git restore file — throws the change away ⚠</span></div>
    <div class="anat-row"><span>In the staging area</span><span>git restore --staged file — unstages, the change stays</span></div>
    <div class="anat-row"><span>In the last commit</span><span>git commit --amend — fixes the last commit</span></div>
    <div class="anat-row"><span>In commits (only yours)</span><span>git reset — moves the branch back</span></div>
    <div class="anat-row"><span>In a shared commit</span><span>git revert — a new commit doing the opposite</span></div>
  </div>
  <figcaption>Ask first: where is the thing I want to undo? The command follows from that.</figcaption>
</figure>

## 1. Throw away a change in a file: `git restore`

You edited a file, didn't like it, and want it back as it was in the last
commit:

```text
~/notes (main) $ echo "oops" > todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git restore todo.txt
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
~/notes (main) $ git status -s
```

`git status` was already saying it: `use "git restore <file>..." to discard
changes`. ⚠ A discarded change does not come back; it was never saved
anywhere.

> Older sources use `git checkout -- file` for the same job. It still works,
> but since `checkout` also does other things like switching branches, Git
> 2.23 introduced the clearer `restore` and `switch`. We will use the new
> ones.

## 2. Unstage: `git restore --staged`

You added a change with `git add` but don't want it in this commit. The
change **stays in the file**; it only leaves the staging area:

```text
~/notes (main) $ echo "Buy eggs" >> todo.txt
~/notes (main) $ git add todo.txt
~/notes (main) $ git status -s
M  todo.txt
~/notes (main) $ git restore --staged todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
Buy eggs
```

This is safe: nothing is deleted. For a new (never committed) file,
`git rm --cached` from section 02 does the same.

## 3. Fix the last commit: `git commit --amend`

The two most common mistakes: a typo in the message, or forgetting to add a
file. Both are fixed by rewriting the last commit.

Changing the message:

```text
~/notes (main) $ git log --oneline -2
820b3f1 (HEAD -> main) Add brad
f2dfe4a Add readme
~/notes (main) $ git commit --amend -m "Add bread"
[main b898dbd] Add bread
 Date: Wed Oct 7 10:04:00 2026 +0300
 1 file changed, 1 insertion(+)
~/notes (main) $ git log --oneline -2
b898dbd (HEAD -> main) Add bread
f2dfe4a Add readme
```

Adding a forgotten file: first `git add`, then `--amend --no-edit` ("leave
the message alone"):

```text
~/notes (main) $ git status -s
?? plan.txt
~/notes (main) $ git log --oneline -1
744ea10 (HEAD -> main) Plan the week
~/notes (main) $ git add plan.txt
~/notes (main) $ git commit --amend --no-edit
[main 17622b9] Plan the week
 Date: Wed Oct 7 10:04:00 2026 +0300
 2 files changed, 2 insertions(+)
 create mode 100644 plan.txt
~/notes (main) $ git log --oneline -1
17622b9 (HEAD -> main) Plan the week
~/notes (main) $ git show --stat
commit 17622b994a10ce90c75bcc8039fb9f3e681d9259 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:04:00 2026 +0300

    Plan the week

 plan.txt | 1 +
 todo.txt | 1 +
 2 files changed, 2 insertions(+)
```

The number of commits stayed the same but the hash changed (`--amend` does
not edit the old commit, it puts a new one in its place). ⚠ So do not
`--amend` a commit you have **shared** with others (sent to GitHub); section
09 shows why.

## 4. Bring back an old version of a file

`git restore --source=<commit> file` brings the file back to how it was in
that commit. Only that file changes; the history stays as it is, and you
commit the change if you want:

```text
~/notes (main) $ git restore --source=HEAD~2 todo.txt
~/notes (main) $ cat todo.txt
Buy milk
~/notes (main) $ git status -s
 M todo.txt
```

## 5. Deleting and renaming tracked files

If you delete a tracked file with `rm`, Git sees a "deleted but not staged"
change and you still need `git add`. `git rm` does both. Same for renaming:
`git mv`.

```text
~/notes (main) $ git mv readme.md README.md
~/notes (main) $ git status -s
R  readme.md -> README.md
~/notes (main) $ rm todo.txt
~/notes (main) $ git status -s
R  readme.md -> README.md
 D todo.txt
~/notes (main) $ git restore todo.txt
~/notes (main) $ git rm todo.txt
rm 'todo.txt'
~/notes (main) $ git status -s
R  readme.md -> README.md
D  todo.txt
~/notes (main) $ ls
README.md
```

## 6. Clean up untracked files: `git clean`

Build output, temporary files... To delete files Git has never tracked in
one go, use `git clean`. To protect you, Git refuses without `-f` (*force*);
**look first with `-n`** at what would be deleted:

```text
~/notes (main) $ git status -s
?? build/
?? cache.tmp
~/notes (main) $ git clean
fatal: clean.requireForce is true and -f not given: refusing to clean
~/notes (main) $ git clean -n
Would remove cache.tmp
~/notes (main) $ git clean -nd
Would remove build/
Would remove cache.tmp
~/notes (main) $ git clean -fd
Removing build/
Removing cache.tmp
~/notes (main) $ git status -s
```

`-d` deletes untracked folders too. ⚠ Files deleted by `git clean` were never
committed; they cannot be brought back.

## 7. Undo commits: `git reset`

`git reset` **moves the branch back**: the last commits leave the branch.
The real question is what happens to the changes in those commits; three
modes decide:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>git reset --soft HEAD~1</span><span>The commit leaves the branch. The change is staged, ready to commit.</span></div>
    <div class="anat-row"><span>git reset HEAD~1</span><span>(--mixed) The commit leaves. The change is in the file, unstaged.</span></div>
    <div class="anat-row"><span>git reset --hard HEAD~1</span><span>The commit leaves and the change is deleted. Files go back to the previous commit. ⚠</span></div>
  </div>
  <figcaption>In all three the branch goes back one commit; the difference is where the change ends up.</figcaption>
</figure>

```text
~/notes (main) $ git log --oneline -2
1d5cec5 (HEAD -> main) Add bread
f2dfe4a Add readme
~/notes (main) $ git reset --soft HEAD~1
~/notes (main) $ git status -s
M  todo.txt
~/notes (main) $ git commit -m "Add bread"
[main b898dbd] Add bread
 1 file changed, 1 insertion(+)
~/notes (main) $ git reset HEAD~1
Unstaged changes after reset:
M       todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git commit -am "Add bread"
[main 9b9aedd] Add bread
 1 file changed, 1 insertion(+)
~/notes (main) $ git reset --hard HEAD~1
HEAD is now at f2dfe4a Add readme
~/notes (main) $ git status -s
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

- `--soft`: the commit is gone, the change waits **in the staging area**.
  For jobs like "turn the last two commits into one".
- `--mixed` (the default when you give no option): the change is **in the
  file**, unstaged.
- ⚠ `--hard`: the change is **gone completely**; the files go back to that
  commit. Your uncommitted work is deleted too.

`git reset --hard` (without a commit) means "throw away everything I did
since the last commit"; ⚠ this is the most dangerous undo.

> Threw away a commit with `reset --hard` and regret it? Commits are not
> deleted right away; in section 14 we will bring them back with
> `git reflog`.

## 8. Undo a shared commit: `git revert`

`reset` changes the history: commits leave the branch. Fine for commits on
your own computer, but if you remove a commit others have already received,
their history and yours split apart.

`git revert <commit>` leaves the history alone: it adds **a new commit that
does the opposite** of that commit.

```text
~/notes (main) $ git revert HEAD --no-edit
[main 3f6b747] Revert "Add bread"
 1 file changed, 1 deletion(-)
~/notes (main) $ git log --oneline -3
3f6b747 (HEAD -> main) Revert "Add bread"
1d5cec5 Add bread
f2dfe4a Add readme
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>git reset HEAD~1</h4><p>A → B → C</p><p>after: A → B</p><p>C left the history</p><p><b>Only for commits that are only yours</b></p></div>
    <div class="ok"><h4>git revert HEAD</h4><p>A → B → C</p><p>after: A → B → C → C'</p><p>C' does the opposite of C</p><p><b>For shared history</b></p></div>
  </div>
  <figcaption>reset removes from history, revert adds to it. In both, the files end up the same.</figcaption>
</figure>

## Which one when?

| Situation | Command |
|---|---|
| Throw away a change in a file | ⚠ `git restore file` |
| Unstage | `git restore --staged file` |
| Fix the last commit's message | `git commit --amend -m "New"` |
| Add a forgotten file to the last commit | `git add file` + `git commit --amend --no-edit` |
| Bring back an old version of a file | `git restore --source=HEAD~2 file` |
| Delete / move a tracked file | `git rm file` / `git mv old new` |
| Delete untracked files | `git clean -n`, then ⚠ `git clean -f` |
| Undo the last commits, keep the changes | `git reset HEAD~1` (`--soft` keeps them staged) |
| Throw away the last commits entirely | ⚠ `git reset --hard HEAD~1` |
| Undo a shared commit | `git revert <commit>` |

## Summary

- Uncommitted work is not protected: `restore`, `clean -f`, `reset --hard`
  delete it for good.
- `restore` works on the file, `restore --staged` on the staging area.
- `--amend` replaces the last commit with a new one; don't use it on a
  shared commit.
- `reset` moves the branch back: `--soft` keeps changes staged, `--mixed` in
  the file, `--hard` throws them away.
- `revert` adds a new commit doing the opposite without breaking history;
  the right way for shared history.
