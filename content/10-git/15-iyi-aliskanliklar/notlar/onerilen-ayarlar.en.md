All the settings to make once on a new computer. What you learned in this
track is added to those from 01 (name, e-mail, branch name, editor).

```text
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

git config --global pull.rebase true
git config --global fetch.prune true
git config --global push.autoSetupRemote true

git config --global alias.lg "log --oneline --graph --all"
git config --global alias.st "status -s"
git config --global alias.last "log -1 --stat"
```

| Setting | Benefit |
|---|---|
| `pull.rebase true` | `pull` asks no question on divergence; it replays local commits on top (12). |
| `fetch.prune true` | Traces of branches deleted on GitHub are cleaned up by themselves (10). |
| `push.autoSetupRemote true` | No `-u origin branch` needed for a new branch's first push. |
| `alias.lg` | `git lg`: all branches at a glance. |
| `alias.st` | `git st`: short status. |
| `alias.last` | `git last`: the last commit and its files. |

## Seeing the settings

```text
git config --global --list
```

All settings live in the `~/.gitconfig` file; when moving to a new computer
you can copy this file too (mind personal things like your e-mail).
