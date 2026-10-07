A good pull request is easy to review and gets merged quickly.

## Before opening

- Was the branch started from the latest `main`? If not, merge `main` into it.
- Does the PR tell **one piece of work**? Two separate jobs, two PRs.
- Any leftover files, debug lines, commented-out code?
- Does the program run, do the tests pass?

## Title and description

The title is like a commit message: short, saying what it does (`Add contact
form`). A template for the description:

```text
## What changed?
A form was added to the contact page; messages arrive by e-mail.

## Why?
Visitors had to copy our e-mail address to reach us.

## How to try it?
1. Open the /contact page
2. Fill in the form and send it

Fixes #12
```

## During review

- Comments are about the code, not the person. When suggesting something,
  write why.
- Make requested changes **on the same branch** and push; the PR updates.
- When you've answered or fixed a comment, **Resolve conversation**.

## After merging

```text
git switch main
git pull
git branch -d branch-name  # -D if it was squash-merged
git fetch --prune
```

## Which merge option?

| Option | In the history | When |
|---|---|---|
| Merge commit | All the branch's commits + a merge commit | When the branch's steps are meaningful. |
| Squash and merge | A single commit | When the branch has many "wip", "fix" commits. |
| Rebase and merge | The branch's commits in a straight line | In teams that want a straight history. |

Teams often pick one and turn the others off in Settings.
