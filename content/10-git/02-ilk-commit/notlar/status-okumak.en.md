Every part of `git status` output and what it means. When you are stuck,
look at this table, then read the command Git suggests in brackets.

## Sections of the long output

| Heading | Meaning | Next step |
|---|---|---|
| `On branch main` | Which branch you are on. | — |
| `No commits yet` | The repository has no commits. | Make the first commit. |
| `Changes to be committed` (green) | In the staging area; goes into the next commit. | `git commit -m "…"` |
| `Changes not staged for commit` (red) | A tracked file changed but is not staged. | `git add <file>` |
| `Untracked files` (red) | A file Git has never tracked. | `git add <file>` or `.gitignore` |
| `nothing to commit, working tree clean` | Everything is committed; no changes. | Keep working. |

## Words at the start of lines

| Word | Meaning |
|---|---|
| `new file:` | New file (in the staging area). |
| `modified:` | Content changed. |
| `deleted:` | Deleted. |
| `renamed:` | Renamed (with `git mv`). |

## Short format (`git status -s`)

```text
 M index.html     right column: modified, not staged
M  about.html     left column: modified, staged
MM style.css      both: staged, then changed again
A  logo.svg       new file, staged
 D old.html       deleted, not staged
?? notes.txt      untracked
```

Rule: **the left column is what goes into the next commit**, **the right
column is what does not**.

## Four states of a file

| State | Where it shows |
|---|---|
| Untracked | `Untracked files`, `??` |
| Staged | `Changes to be committed`, left column |
| Modified | `Changes not staged…`, right column |
| Unmodified | Nowhere: same as in the commit |

Unmodified files do not show in `git status`; Git only shows
**differences**. A file missing from the list means "all is well".
