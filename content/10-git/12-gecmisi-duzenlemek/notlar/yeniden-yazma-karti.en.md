The commands that rewrite history, and how to use them safely.

| Command | What it does | On shared commits? |
|---|---|---|
| `git commit --amend` | Replaces the last commit with a new one. | ⚠ No |
| `git reset HEAD~n` | Takes the last n commits off the branch. | ⚠ No |
| `git rebase main` | Replays the branch's commits on the tip of main. | ⚠ No |
| `git rebase -i HEAD~n` | Edits the last n commits (squash, reword, drop). | ⚠ No |
| `git pull --rebase` | Replays local commits on top of incoming ones. | Yes (only your unpushed commits change) |
| `git cherry-pick X` | Adds a copy of X to the branch you are on. | Yes (adds a new commit) |
| `git revert X` | Adds a commit doing the opposite of X. | Yes |

## During a rebase

| Situation | Command |
|---|---|
| I resolved the conflict | `git add file` → `git rebase --continue` |
| Skip this commit | `git rebase --skip` |
| I changed my mind | `git rebase --abort` |
| Where am I? | `git status` (lists the done and remaining commits) |

## During a cherry-pick

| Situation | Command |
|---|---|
| I resolved the conflict | `git add file` → `git cherry-pick --continue` |
| I changed my mind | `git cherry-pick --abort` |
| Several commits | `git cherry-pick A B C` or a range `A^..C` |

## If you must force-push

To overwrite the old version on GitHub after rebasing your own branch (one
only you work on):

```text
git push --force-with-lease
```

`--force-with-lease`, not `--force`: if someone else pushed to that branch
since your last `fetch`, it refuses, so you don't overwrite their work.
