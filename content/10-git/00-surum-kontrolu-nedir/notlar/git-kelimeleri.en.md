Words that come up constantly in this track. You don't need to memorise them
now; each is explained in detail in its own section. Come back here when a
word trips you up.

| Word | Meaning | Section |
|---|---|---|
| **repository** (repo) | The folder Git watches; the history is in `.git`. | 00 |
| **commit** | A snapshot of the project: change + author + date + message. | 02 |
| **commit message** | A short sentence saying why the commit was made. | 02 |
| **working tree** | How the files in the folder look right now. | 02 |
| **staging area** (index) | Where the changes for the next commit are gathered. | 02 |
| **hash** | A commit's unique id: a letter-digit string like `6fb3238`. | 03 |
| **diff** | The line-by-line difference between two states. | 03 |
| **branch** | A separate line of history; you experiment on it, then merge. | 06 |
| **main** | The usual name of a repository's main branch (formerly `master`). | 06 |
| **HEAD** | The "where am I" marker; usually the last commit of your branch. | 06 |
| **merge** | Bringing the changes of two branches together. | 07 |
| **conflict** | Two branches changed the same line differently; you choose. | 08 |
| **remote** | A copy of the repository somewhere else, usually on GitHub. | 09 |
| **origin** | The default name of the remote you cloned from. | 09 |
| **clone** | Downloading a remote repository with its history. | 09 |
| **push / pull** | Sending commits to the remote / getting them from it. | 09 |
| **pull request** (PR) | A request on GitHub: "would you merge my branch?" | 10 |
| **fork** | Your own copy on GitHub of someone else's repository. | 10 |
| **stash** | Putting unfinished work aside without committing. | 11 |
| **rebase** | Replaying commits on top of another commit. | 12 |
| **tag** | A permanent name for a commit, e.g. `v1.0`. | 13 |
| **reflog** | A record of everywhere HEAD has been; how you find lost work. | 14 |

## The general shape of a command

All Git commands follow the same pattern:

```text
git <subcommand> [options] [targets]
git commit -m "Add readme"
git log --oneline -n 3
```

- The first word after `git` says what to do (`commit`, `log`).
- There are short options with one dash like `-m`, `-n`, and long options
  with two dashes like `--oneline`.
- If you forget what to type, `git <subcommand> -h` shows a short help (in a
  real terminal).
