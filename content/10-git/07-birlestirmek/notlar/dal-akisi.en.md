Most teams use branches and merging in the same pattern. It is called the
**feature branch workflow**; pull requests on GitHub (10) build on it.

## Rules

1. `main` always works. Nobody commits to it directly.
2. Each piece of work gets a new branch from `main`: `git switch -c
   contact-form`.
3. The work happens on that branch, in small, meaningful commits.
4. If the work takes long, `main` is merged into the branch now and then; the
   branch stays up to date.
5. When the work is done, the branch is merged into `main` (in teams via a
   pull request, after someone reviews it).
6. The merged branch is deleted.

## A day's flow

```text
git switch main                  back to the main branch
git switch -c contact-form       a branch for the new work
... edit, git add, git commit (a few times) ...
git switch main                  back to the main branch
git merge contact-form --no-edit take the work
git branch -d contact-form       clean up the branch
```

## Why so many branches?

- **Half-done work doesn't break `main`.** If something goes wrong, you delete
  the branch and start over.
- **Several pieces of work run at once.** When an urgent bug comes in, you
  leave the half-done branch and open a new one from `main`.
- **Reviewing gets easier.** One branch tells one piece of work; your teammate
  reviews only that.

## Long-lived branches

Some teams keep another long-lived branch like `develop` next to `main` (*Git
Flow*). Small projects don't need it; a single `main` and short-lived feature
branches are usually enough. The shorter branches live, the easier merging
gets.
