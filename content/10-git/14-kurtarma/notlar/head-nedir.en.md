HEAD is Git's "I am here" marker. Most of the time it points to a
**branch**:

```text
HEAD → main → 63074be
```

When you commit, `main` moves to the new commit, and since HEAD points to
`main`, it goes along. The prompt says `(main)`.

## The detached state

If you switch directly to a commit instead of a branch (`git checkout
63074be`, `git checkout v1.0`, `git checkout HEAD~2`):

```text
HEAD → c1a230e        (no branch in between)
```

When you commit, HEAD moves to the new commit but **no branch moves**. When
you switch to another branch, no name is left pointing to the new commit;
that's why Git warns you.

## How do you end up in a detached HEAD?

| Command | Why |
|---|---|
| `git checkout <hash>` | You switched to a commit. |
| `git checkout v1.0` | A tag isn't a branch. |
| `git checkout origin/main` | A remote-tracking branch isn't your branch. |
| `git switch --detach <commit>` | On purpose. |
| During a rebase | While replaying commits Git is on no branch (temporary). |

## Getting out of a detached HEAD

| What do you want? | Command |
|---|---|
| I did nothing, go back | `git switch -` or `git switch main` |
| Keep what I did here | `git switch -c new-branch` |
| I went back but commits were left | The command from the warning: `git branch name <hash>` |

## `HEAD@{n}` versus `HEAD~n`

- `HEAD~2`: two commits back in history (the parent's parent).
- `HEAD@{2}`: where HEAD was **two moves ago** (from the reflog). A checkout
  or a reset also counts as a move; it may not be a commit.
