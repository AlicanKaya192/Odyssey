All the branch commands in one place.

## Seeing

| Command | Shows |
|---|---|
| `git branch` | Local branches; `*` is the one you are on. |
| `git branch -v` | With each branch's last commit. |
| `git branch -a` | Together with the remote's branches (09). |
| `git branch --merged` | Those merged into the branch you are on. |
| `git branch --no-merged` | Those not merged yet. |
| `git log --oneline --graph --all` | The history of all branches, with lines. |

## Creating and switching

| Command | What it does |
|---|---|
| `git branch name` | Creates a branch at the current commit, doesn't switch. |
| `git branch name <commit>` | Creates a branch at a given commit. |
| `git switch name` | Switches to the branch. |
| `git switch -c name` | Creates and switches. |
| `git switch -c name <commit>` | Creates from a given commit and switches. |
| `git switch -` | Goes back to the previous branch. |
| `git checkout name` / `git checkout -b name` | The old forms. |

## Managing

| Command | What it does |
|---|---|
| `git branch -m new` | Renames the branch you are on. |
| `git branch -m old new` | Renames another branch. |
| `git branch -d name` | Deletes it if merged. |
| `git branch -D name` | ⚠ Force-deletes. |

## Common errors

| Message | Meaning | Fix |
|---|---|---|
| `fatal: invalid reference: x` | No such branch. | Check its name with `git branch`; use `-c` to create it. |
| `fatal: a branch named 'x' already exists` | A branch with that name exists. | Another name, or `git switch x`. |
| `Your local changes ... would be overwritten` | An uncommitted change differs on the target branch. | Commit first, or `git stash`. |
| `the branch 'x' is not fully merged` | The branch has commits that exist nowhere else. | Merge first; if you really mean it, `-D`. |
| `cannot delete branch 'x' used by worktree` | You are deleting the branch you are on. | Switch to another branch. |
| `cannot lock ref ... exists` | You tried `feature/x` while `feature` exists. | Pick a different name. |
