All the commands of the track on one page.

## Getting started

| Command | What it does |
|---|---|
| `git init` | Makes the folder a repository. |
| `git clone <url>` | Downloads a remote repository. |
| `git config --global user.name "Name"` | Identity (once). |

## Every day

| Command | What it does |
|---|---|
| `git status` / `-s` | The state. |
| `git add file` / `.` | Stage. |
| `git commit -m "Message"` | Commit. |
| `git diff` / `--staged` | The difference. |
| `git log --oneline --graph --all` | The history. |
| `git pull` / `git push` | Take / send. |

## Branches

| Command | What it does |
|---|---|
| `git switch -c branch` | Create and switch. |
| `git switch branch` / `-` | Switch / go back. |
| `git merge branch` | Merge into the branch you are on. |
| `git branch -d branch` / `-D` | Delete / force-delete. |
| `git rebase main` | Move onto a new base (only a branch that is only yours). |
| `git cherry-pick X` | Copy a single commit. |

## Undoing

| Command | What it does |
|---|---|
| `git restore file` | ⚠ Throw away the change in a file. |
| `git restore --staged file` | Unstage. |
| `git commit --amend` | Fix the last commit. |
| `git reset --soft / --mixed / --hard HEAD~1` | Undo a commit. |
| `git revert X` | Undo a shared commit. |
| `git stash` / `pop` | Put aside / bring back. |
| `git reflog` | Find what was lost. |

## Remotes and releases

| Command | What it does |
|---|---|
| `git remote add origin <url>` | Save a remote. |
| `git push -u origin branch` | Push a branch for the first time. |
| `git fetch --prune` | Get news, clean up deleted branches. |
| `git tag -a v1.0 -m "..."` | A release tag. |
| `git push --tags` | Push tags. |

## State markers

| If you see | It means | Way out |
|---|---|---|
| <code>(main&#124;MERGING)</code> | A merge is half-done | resolve + commit, or `git merge --abort` |
| <code>(main&#124;REBASE)</code> | A rebase is half-done | resolve + `git rebase --continue`, or `--abort` |
| `(1a2b3c4...)` | Detached HEAD | `git switch -c new` or `git switch -` |
