## Commands

| Command | What it does |
|---|---|
| `git merge branch` | Merges `branch` into the branch you are on. |
| `git merge branch --no-edit` | With the ready-made message, no editor. |
| `git merge branch -m "message"` | With your own message. |
| `git merge --no-ff branch` | A merge commit even if a fast-forward is possible. |
| `git merge --abort` | Cancels an unfinished (conflicted) merge (08). |
| `git branch --merged` | Merged branches, safe to delete. |
| `git log --oneline --graph` | See the merge as lines. |

## Direction

The command changes **the branch you are on**:

| What do you want? | First | Then |
|---|---|---|
| Bring my branch's work into main | `git switch main` | `git merge mybranch` |
| Bring what's new on main into my branch | `git switch mybranch` | `git merge main` |

## Two forms

| | Fast-forward | Three-way |
|---|---|---|
| When | The target branch hasn't moved since the split | Both branches moved |
| New commit | None; the label slides | A merge commit (two parents) |
| In the output | `Fast-forward` | `Merge made by the 'ort' strategy.` |
| Graph | A straight line | A fork with <code>&#124;\</code> and <code>&#124;/</code> |
| Can it conflict? | No | Yes, if the same line changed on both |

`ort` is the name of Git's current merge method (*Ostensibly Recursive's
Twin*). Older output says `recursive`; same job.

## Common messages

| Message | Meaning |
|---|---|
| `Already up to date.` | Everything on that branch is already here. |
| `merge: x - not something we can merge` | No such branch or commit; check the name. |
| `CONFLICT (content): Merge conflict in a.txt` | A conflict; section 08. |
| `error: Your local changes ... would be overwritten by merge` | An uncommitted change blocks the merge; commit or stash first. |
