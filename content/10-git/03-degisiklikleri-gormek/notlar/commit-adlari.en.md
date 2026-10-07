Ways to name a commit for Git. All of them can be written instead of a hash
in commands like `git show`, `git diff` and `git log`.

| Name | Meaning |
|---|---|
| `1158a1b7fc12…` | The full hash (40 characters). |
| `1158a1b` | A short hash; enough as long as it matches one commit (usually 7 characters). |
| `HEAD` | The commit you are on right now. |
| `HEAD~1` | The one before HEAD (its parent). `HEAD~` is the same. |
| `HEAD~3` | Three before. |
| `main` | The last commit of the `main` branch. |
| `main~2` | Two before the last commit of `main`. |
| `v1.0` | The commit a tag points to (section 13). |

## Why does a hash look like that?

A hash is a **fingerprint** computed from the commit's content (files,
author, date, message, previous commit). Two consequences:

- The same content always gives the same hash; different content a
  different one. Nobody can quietly change a commit without changing its
  hash.
- A commit's hash also depends on the hash of the commit before it. If
  something changes in the past, the hash of every later commit changes.
  (`rebase` and `--amend` will do this in section 12.)

That is why the hashes in the lesson come out different in your terminal:
the date and author differ.

## `~` versus `^`

`HEAD~2` means "two steps back along the first parent". `^` chooses which
parent of a merge commit: `HEAD^1` is the first parent, `HEAD^2` the second
(the merged branch). In a history without merges, `HEAD^` and `HEAD~` are
the same. We will see merging in section 07.
