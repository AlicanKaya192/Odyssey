## Connecting

| Command | What it does |
|---|---|
| `git clone <url>` | Downloads the repository with its history, sets up `origin`. |
| `git clone <url> folder` | Downloads into a different folder name. |
| `git remote -v` | The saved remotes and their addresses. |
| `git remote add origin <url>` | Saves a remote. |
| `git remote set-url origin <new>` | Changes the address. |
| `git remote remove origin` | Removes the entry (doesn't touch the repository on GitHub). |

## Sending

| Command | What it does |
|---|---|
| `git push -u origin main` | The first push; sets up tracking. |
| `git push` | Pushes to the tracked branch. |
| `git push -u origin branch` | Pushes a new branch for the first time. |
| `git push origin --delete branch` | Deletes the branch on GitHub. |
| `git push --tags` | Pushes tags (13). |
| ⚠ `git push --force-with-lease` | Pushes rewritten history; refuses if someone else pushed. |

## Taking

| Command | What it does |
|---|---|
| `git fetch` | Downloads what's new, updates the `origin/...` branches; doesn't touch your branch. |
| `git pull` | fetch + merge. |
| `git pull --no-rebase` | Take diverged branches with a merge. |
| `git pull --rebase` | Take diverged branches by replaying (12). |
| `git config --global pull.rebase false` | Make `pull` always merge (once). |

## Seeing the state

| Command | Shows |
|---|---|
| `git status` | `ahead` / `behind` / `diverged` (as of the last fetch). |
| `git branch -vv` | Each branch's tracked remote branch and ahead / behind counts. |
| `git branch -a` | All branches including remote-tracking ones. |
| `git log --oneline --all --graph` | Your history and the remote branches together. |

## Common messages

| Message | Meaning | What to do |
|---|---|---|
| `Your branch is ahead of 'origin/main' by N commits` | You have commits you haven't pushed. | `git push` |
| `Your branch is behind 'origin/main' by N commits` | There are commits you haven't taken. | `git pull` |
| `have diverged` | Both sides moved. | `git pull --no-rebase`, then `git push` |
| `! [rejected] ... (fetch first)` | GitHub has commits you don't know about. | `git pull`, then `git push` |
| `has no upstream branch` | The branch is pushed for the first time. | `git push -u origin branch` |
| `Repository not found` | Wrong address, or no repository / no access. | Check the address and GitHub. |
