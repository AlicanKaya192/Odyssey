`git log --oneline --graph --all` shows how branches split and join with
text lines. Busy at first sight; knowing four marks is enough.

| Mark | Meaning |
|---|---|
| `*` | A commit. The rest of the line is its hash and message. |
| <code>&#124;</code> | A branch's line; it flows down towards the past. |
| `/` | A branch split off here (forked from the commit below). |
| `\` | A branch joined here (a merge, 07). |

## An example

```text
* 4c1a2f0 (login) Add login form
| * 9e8d7c6 (HEAD -> main) Fix typo
|/
* 2b3c4d5 Add home page
```

Read from the bottom up (old to new):

1. `Add home page` is the common point of the two branches.
2. Two lines come out of it (`|/`): one is `main`, one is `login`.
3. `main` has `Fix typo`, `login` has `Add login form`; the two branches don't
   see each other's commits.
4. The names in brackets say where the branches are right now. `HEAD -> main`
   is the branch you are on.

## Tips

- Without `--all` you only see the history of the branch you are on; the
  other branches aren't drawn.
- In a long history, add a limit like `-10`.
- If you type this often you can define a shortcut (in 15):
  `git config --global alias.lg "log --oneline --graph --all"`, then
  `git lg`.
