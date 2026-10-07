There is no right or wrong between merge and rebase; a team picks a pattern
and sticks to it. These questions help you decide.

| Question | Merge | Rebase |
|---|---|---|
| What does the history look like? | As it really happened: branches and merge points | A straight line, as if everything was done in order |
| Do commits change? | No | Yes, new hashes |
| Safe on a shared branch? | Yes | No |
| How many times is a conflict resolved? | Once, at the merge | Possibly once per commit |
| Reading `git log` | Merge commits can add clutter | Easy |

## A common pattern

1. Work on a feature branch.
2. If `main` moved on, keep your branch up to date: `git fetch` + `git rebase
   origin/main` (if the branch is only yours) or `git merge origin/main`.
3. Open a PR; merge on GitHub (with the method the team chose).
4. Update your own `main` with `git pull` (with `pull.rebase true` it makes no
   difference if you have no local commits).

## When definitely merge?

- If the branch is shared with others.
- When joining long-lived branches like `main` and `develop`.
- If keeping "what really happened" in the history matters.

## When is rebase comfortable?

- `git pull --rebase` while you have local commits not pushed yet.
- Cleaning up a branch only you work on, before a PR.
