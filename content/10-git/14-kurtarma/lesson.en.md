# Recovery: reflog and Detached HEAD

You threw away three commits with `git reset --hard`, deleted an unmerged
branch with `-D`, or somewhere it said "detached HEAD" and your commits
vanished... Good news: **committed work is almost never lost in Git.**
Commits that drop off a branch stay in the repository for a while. The way to
find them is the **reflog**.

## Detached HEAD

Normally HEAD points to a **branch**, and the branch to a commit. When you
commit, the branch moves. But if you switch directly to a **commit** (or a
tag) instead of a branch, HEAD gets detached:

```text
~/app (main) $ git checkout HEAD~1
Note: switching to 'HEAD~1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 1c20e46 Two
~/app (1c20e46...) $ git status
HEAD detached at 1c20e46
nothing to commit, working tree clean
~/app (1c20e46...) $ cat f.txt
1
2
```

Git writes a long explanation; in short: "You can look around and experiment;
but commits you make here belong to no branch." The prompt also shows
a short hash and three dots instead of a branch.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Normal</h4><p>HEAD → main → commit</p><p>Committing moves main</p><p>Prompt: (main)</p></div>
    <div class="no"><h4>Detached HEAD</h4><p>HEAD → commit</p><p>Committing moves no branch</p><p>Prompt: (c1a230e...)</p></div>
  </div>
  <figcaption>Looking around in a detached HEAD is safe; if you'll work there, create a branch first with git switch -c.</figcaption>
</figure>

Detached HEAD is safe and handy for **looking at an old state**. The trouble
starts if you commit there and then go back to a branch:

```text
~/app (1c20e46...) $ echo "e" > e.txt
~/app (1c20e46...) $ git add .
~/app (1c20e46...) $ git commit -m "Experiment"
[detached HEAD 95e02d2] Experiment
 1 file changed, 1 insertion(+)
 create mode 100644 e.txt
~/app (95e02d2...) $ git switch main
Warning: you are leaving 1 commit behind, not connected to
any of your branches:

  95e02d2 Experiment

If you want to keep it by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> 95e02d2

Switched to branch 'main'
~/app (main) $ git branch experiment HEAD@{1}
~/app (main) $ git log --oneline experiment -2
95e02d2 (experiment) Experiment
1c20e46 Two
```

Git warned: the `Experiment` commit isn't connected to any branch. If you do
what the warning says (`git branch <name> <hash>`), the commit is saved.
Better: if you'll work in a detached HEAD, **create a branch first**:
`git switch -c experiment`.

## reflog: HEAD's diary

Git records **everywhere** HEAD goes: commit, checkout, reset, merge,
rebase... This record is the **reflog** (*reference log*). `git log` shows
the branch's history; `git reflog` shows **what you did**:

```text
~/app (main) $ git reflog
be3b130 (HEAD -> main, test) HEAD@{0}: checkout: moving from test to main
be3b130 (HEAD -> main, test) HEAD@{1}: checkout: moving from main to test
be3b130 (HEAD -> main, test) HEAD@{2}: commit: Three
1c20e46 HEAD@{3}: commit: Two
8ba380a HEAD@{4}: commit (initial): One
```

Each line: the commit at that moment, `HEAD@{n}` (where HEAD was n moves
ago) and what happened. `HEAD@{0}` is now, `HEAD@{1}` the previous move. These
names can be used instead of a commit in any command.

## Recovery 1: undoing a `reset --hard`

You threw away commits with `reset --hard`:

```text
~/app (main) $ git reset --hard HEAD~2
HEAD is now at 8ba380a One
~/app (main) $ git log --oneline
8ba380a (HEAD -> main) One
~/app (main) $ git reflog -3
8ba380a (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
be3b130 HEAD@{1}: commit: Three
1c20e46 HEAD@{2}: commit: Two
~/app (main) $ git reset --hard HEAD@{1}
HEAD is now at be3b130 Three
~/app (main) $ git log --oneline
be3b130 (HEAD -> main) Three
1c20e46 Two
8ba380a One
```

`git log` now shows only `One`, but the reflog remembers everything:
`HEAD@{1}` is the state right before the reset. `git reset --hard HEAD@{1}`
took the branch back there.

## Recovery 2: a deleted branch

You deleted the unmerged `temp` branch with `-D`. The branch was just a
label; its commits are still there. Find the branch's last commit in the
reflog and create a new branch there:

```text
~/app (main) $ git reflog -3
be3b130 (HEAD -> main) HEAD@{0}: checkout: moving from temp to main
f46d820 HEAD@{1}: commit: Temp work
be3b130 (HEAD -> main) HEAD@{2}: checkout: moving from main to temp
~/app (main) $ git branch temp HEAD@{1}
~/app (main) $ git log --oneline temp -2
f46d820 (temp) Temp work
be3b130 (HEAD -> main) Three
```

## What can't you recover?

The reflog only knows **committed** states:

| Situation | Recoverable? |
|---|---|
| Commits thrown away with `reset --hard` | Yes, reflog. |
| A branch deleted with `-D` | Yes, reflog + `git branch`. |
| Commits made in a detached HEAD and forgotten | Yes, reflog. |
| A wrong `rebase` or `--amend` | Yes: the old state is in the reflog (`HEAD@{n}`). |
| Uncommitted changes (`restore`, `reset --hard`, `clean -f`) | ⚠ No. |
| `git stash drop` / `clear` | Very hard (with special tools). |

The lesson: **commit** before doing something you are unsure about (you can
fix it afterwards with `--amend` or `reset --soft`).

> The reflog lives **only on your computer**, doesn't go to GitHub, and isn't
> permanent: Git cleans old entries after a while (by default 90 days, 30
> days for ones that fell off a branch). Don't delay a recovery.

## In a panic

1. **Stop.** Don't type other commands; especially not `reset --hard` or
   `clean`.
2. `git status`: is an operation half-done (MERGING, REBASE)? If so,
   `--abort` is usually the safest way out.
3. `git reflog`: find the state you think you lost (you'll recognise it by
   its message).
4. **Create a branch** at that commit (`git branch rescue HEAD@{3}`) or move
   your branch there (`git reset --hard HEAD@{3}`).
5. Check with `git log --oneline rescue` that you're in the right place.

## Summary

- Detached HEAD: you switched to a commit, not a branch; looking is safe, but
  `git switch -c` first if you'll work there.
- When leaving a detached HEAD, Git lists orphaned commits and the command
  to save them.
- `git reflog` keeps every move of HEAD; `HEAD@{n}` is n moves ago.
- Thrown-away commits: `git reset --hard HEAD@{n}`; a deleted branch: `git
  branch name HEAD@{n}`.
- Uncommitted work isn't in the reflog.
