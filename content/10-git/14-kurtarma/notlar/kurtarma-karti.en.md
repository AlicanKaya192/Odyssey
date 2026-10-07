## What got lost, and how does it come back?

| What happened? | Recovery |
|---|---|
| Commits gone with `git reset --hard HEAD~n` | `git reflog` → `git reset --hard HEAD@{1}` |
| A branch deleted with `git branch -D branch` | `git reflog` → the branch's last commit → `git branch branch <hash>` |
| I committed in a detached HEAD and went back to a branch | `git branch rescue <hash>` with the hash from the warning, or `git reflog` |
| I broke the last commit with `--amend` | `git reset --hard HEAD@{1}` (before the amend) |
| A rebase messed everything up (finished) | `git reflog` → the line before `rebase (start)` → `git reset --hard HEAD@{n}` |
| A rebase is in progress and messed up | `git rebase --abort` |
| A merge is in progress and messed up | `git merge --abort` |
| I threw away an uncommitted change in a file | ⚠ Not recoverable |

## Reading a reflog line

```text
63074be HEAD@{3}: reset: moving to HEAD~2
```

`63074be` is the commit at that moment, `HEAD@{3}` three moves ago, `reset:
moving to HEAD~2` what was done. You find the state you're after on the line
**before the move**: the state before a reset is one line below the reset
line.

## Commands

| Command | What it does |
|---|---|
| `git reflog` | Every move of HEAD. |
| `git reflog -10` | The last 10 moves. |
| `git log --oneline HEAD@{2}` | The history at that moment. |
| `git show HEAD@{2}` | The commit at that moment. |
| `git branch rescue HEAD@{2}` | Create a branch at that moment (the safest). |
| `git reset --hard HEAD@{2}` | Move your branch there (deletes uncommitted work). |
| `git switch -c name` | In a detached HEAD, create a branch here. |
| `git switch -` | Go back to the branch from before the detached HEAD. |

## The golden rule

When recovering, **create a branch** first, then look. Creating a branch
deletes nothing; if it's in the wrong place you delete the branch and nothing
else changes.
