| Command | What it does |
|---|---|
| `git tag v1.0` | A lightweight tag on the commit you are on. |
| `git tag -a v1.0 -m "Version 1.0"` | An annotated tag (for releases). |
| `git tag v0.9 <commit>` | A tag on an old commit. |
| `git tag` / `git tag -l "v1.*"` | List / filter by pattern. |
| `git tag -n` | List with messages. |
| `git show v1.0` | Tag and commit details. |
| `git tag -d v1.0` | Delete the local tag. |
| `git push origin v1.0` | Push one tag to GitHub. |
| `git push --tags` | Push all tags. |
| `git push origin --delete v1.0` | Delete the tag on GitHub. |
| `git describe` | Position relative to the nearest annotated tag. |
| `git checkout v1.0` | Look at the code at the tag (detached HEAD). |
| `git switch -c fix-1.0 v1.0` | Create a branch from the tag. |
| `git diff v1.0 v1.1` | The difference between two versions. |
| `git log --oneline v1.0..v1.1` | The commits between two versions. |

## Common mistakes

| Message | Meaning | Fix |
|---|---|---|
| `fatal: tag 'v1.0' already exists` | A tag with that name exists. | Another name, or `git tag -d` first. |
| The tag doesn't show on GitHub | `git push` doesn't push tags. | `git push origin v1.0` |
| `git switch v1.0` fails | A tag isn't a branch. | `git checkout v1.0` or `git switch -c branch v1.0` |
| `No annotated tags can describe` | There are only lightweight tags. | `git describe --tags` |

## Ranges with `..`

`git log v1.0..v1.1` means "commits in v1.1 that aren't in v1.0": what was
done between two versions. Handy when writing release notes.
