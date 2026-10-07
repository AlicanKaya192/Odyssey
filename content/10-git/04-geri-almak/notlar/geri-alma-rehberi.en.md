Ask these in order when "I broke something". Commands marked ⚠ permanently
delete uncommitted work.

## The change is not committed yet

| What do you want? | Command |
|---|---|
| Throw away a change in one file | ⚠ `git restore file` |
| Throw away changes in all files | ⚠ `git restore .` |
| Undo `git add` (keep the change) | `git restore --staged file` |
| Unstage a new file | `git rm --cached file` |
| Delete untracked files | `git clean -n` → ⚠ `git clean -f` (`-d` for folders) |
| Put everything back to the last commit | ⚠ `git reset --hard` |

## The last commit has a problem (not shared yet)

| What do you want? | Command |
|---|---|
| Fix the message | `git commit --amend -m "Right message"` |
| Add a forgotten file | `git add file` + `git commit --amend --no-edit` |
| Undo the commit, keep the change staged | `git reset --soft HEAD~1` |
| Undo the commit, keep the change in the file | `git reset HEAD~1` |
| Throw the commit away completely | ⚠ `git reset --hard HEAD~1` |

## The commit was shared (on GitHub, with others)

| What do you want? | Command |
|---|---|
| Undo the effect of a commit | `git revert <commit>` |
| Undo the last commit | `git revert HEAD` |

Don't use `--amend` or `reset` on shared commits: others' history and yours
would split apart.

## An old version of a file

| What do you want? | Command |
|---|---|
| Just look | `git show HEAD~2:file` |
| Bring the file back to it | `git restore --source=HEAD~2 file` |

## The three modes of `reset` in one table

| Mode | Branch | Staging area | Files |
|---|---|---|---|
| `--soft` | moves back | change is there | unchanged |
| `--mixed` (default) | moves back | cleared | change is there |
| ⚠ `--hard` | moves back | cleared | back to the commit, change gone |
