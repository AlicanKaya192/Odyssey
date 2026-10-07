## Commands

| Command | What it does |
|---|---|
| `git stash` | Puts away changes in tracked files. |
| `git stash -u` | Puts away untracked files too. |
| `git stash push -m "message"` | Puts away with a message. |
| `git stash list` | The entries (`stash@{0}` is the newest). |
| `git stash show` / `show -p` | File summary / the full diff. |
| `git stash pop` | Applies the newest and removes it. |
| `git stash apply stash@{n}` | Applies, doesn't remove. |
| `git stash drop stash@{n}` | Removes without applying. |
| ⚠ `git stash clear` | Removes all. |

## Patterns

**An urgent job:**

```text
git stash
git switch main
git switch -c fix-typo
... fix, commit ...
git switch -
git stash pop
```

**I started on the wrong branch:**

```text
git stash
git switch right-branch
git stash pop
```

**A pull was blocked** ("Your local changes ... would be overwritten"):

```text
git stash
git pull
git stash pop
```

## Watch out

- On a clean working tree `git stash` says `No local changes to save`; it
  puts nothing away.
- On a conflict `pop` doesn't remove the entry; after resolving, `git stash
  drop`.
- Stashes removed with `clear` or `drop` don't come back (very hard to
  recover).
- Don't forget work in the stash: if `git stash list` isn't empty, check
  what's in it.
