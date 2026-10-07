There are three ways to park half-done work. Which fits depends on how long
it will wait.

| Way | How | When |
|---|---|---|
| **Stash** | `git stash` … `git stash pop` | Minutes, a few hours. |
| **WIP commit** | `git commit -am "WIP"` … later `git reset --soft HEAD~1` or `--amend` | End of the day, switching computers (can be pushed). |
| **Separate branch** | `git switch -c experiment` + commit | Days; an experiment that may never be merged. |

## Fixing a WIP commit

If you committed half-done work as `WIP` at the end of the day, the next day:

```text
git reset --soft HEAD~1     undo the commit, keep the change staged
... finish the work ...
git commit -m "Add contact form"
```

Or when the work is done, `git commit --amend -m "Add contact form"`. Both
only if the commit hasn't been shared yet (09).

## Working on two branches at once

If you keep jumping between two branches, Git's `worktree` feature opens a
second branch of the same repository **in a separate folder**:

```text
git worktree add ../site-fix fix-typo
```

Now the `../site-fix` folder is on the `fix-typo` branch; the main folder stays
on its own branch, no stash needed. An advanced tool; it's enough to know it
exists.
