The messages you see most in your first commits, their causes and fixes.

| Message | Cause | Fix |
|---|---|---|
| `fatal: not a git repository` | You are in a folder that is not a repository. | Check where you are with `pwd`; `cd` into the right folder or `git init`. |
| `nothing to commit, working tree clean` | There is no change to commit. | Change a file first. |
| `nothing added to commit but untracked files present` | There are new files but none was added. | `git add <file>`, then commit. |
| `no changes added to commit` | The changes are not staged. | `git add` or `git commit -am`. |
| `fatal: pathspec 'x' did not match any files` | The name you gave `git add` does not exist. | Check the name with `ls` (case, extension). |
| `Author identity unknown` | Name and e-mail are not set. | Section 01: `git config --global user.name …` |
| `error: pathspec 'Home' did not match any file(s) known to git` | You typed `-m Add Home` instead of `-m "Add Home"`; Git took `Home` for a file name. | Put the message in quotes. |

## The first commit step by step

```text
git init                          once, if there is no repository
git status                        what is there?
git add index.html                choose what goes into the commit
git status                        is it right?
git commit -m "Add home page"     take the snapshot
git log --oneline                 see it in the history
```

## Ask before you commit

- **Does this commit tell one piece of work?** Two separate jobs, two
  commits.
- **Is anything staged that shouldn't be?** Passwords, big data, temporary
  files.
- **Does the message tell a stranger what happened?** Not `Fix bug` but
  `Fix crash when the list is empty`.
