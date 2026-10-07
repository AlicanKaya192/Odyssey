# Branches

So far every commit was on a single line. In real projects several pieces of
work run at once: you are writing a new feature when an urgent bug turns up.
You need to fix and ship the bug while the feature is half done, and the
half-done work must not get in the way.

Git's answer is the **branch**: a separate line of history. Each branch
collects its own commits and leaves the others alone. You experiment on a
branch; if you like it you merge it into the main branch (07), if not you
delete the branch.

## A branch is really a label

In Git a branch is **a name that points to a commit**, nothing more. Creating
a branch does not copy the folder; it only creates a small marker. That is
why creating a branch is instant and takes no space.

<figure class="fig">
  <div class="flow">
    <span class="node">Add home page</span><span class="arrow">→</span>
    <span class="node">Add styles</span><span class="arrow">→</span>
    <span class="node acc">Add login form<br><small>login ← HEAD</small></span>
  </div>
  <figcaption>Branches are labels pointing to commits. Committing on login moved only the login label; main stayed where it was.</figcaption>
</figure>

When you commit, **the label of the branch you are on** moves to the new
commit. **HEAD** answers "which branch am I on right now"; the `(main)` in the
prompt shows the same thing.

## Seeing and creating branches

```text
~/site (main) $ git branch
* main
~/site (main) $ git branch login
~/site (main) $ git branch
  login
* main
~/site (main) $ git branch -v
  login 7085b6f Add styles
* main  7085b6f Add styles
```

- `git branch` lists the branches; `*` is the one you are on.
- `git branch login` **creates** a new branch **but does not switch**: you
  are still on `main`.
- `git branch -v` also shows the commit each branch points to. Both point to
  the same commit: a new branch starts where it was created.

## Switching to a branch: `git switch`

```text
~/site (main) $ git switch login
Switched to branch 'login'
~/site (login) $ echo "<form>" > login.html
~/site (login) $ git add login.html
~/site (login) $ git commit -m "Add login form"
[login 8072547] Add login form
 1 file changed, 1 insertion(+)
 create mode 100644 login.html
~/site (login) $ git branch -v
* login 8072547 Add login form
  main  7085b6f Add styles
```

Now we are on the `login` branch (the prompt says `(login)`). The commit made
here moved only this branch; `main` stayed where it was.
`git log --oneline --all --graph` draws all branches together:

```text
~/site (main) $ git log --oneline --graph --all
* 0bb20c6 (HEAD -> main) Fix typo
| * 8072547 (login) Add login form
|/  
* 7085b6f Add styles
* a0cf655 Add home page
```

Creating and switching is so common that it has a shortcut:

```bash
git switch -c contact     # -c: create, then switch
```

> The old form: `git checkout -b contact`. Most examples online use it; it
> does the same thing.

## Switching branches changes the files

Switching to a branch brings the files in the folder to **how they are in
that branch's last commit**. A file added on `login` doesn't exist on `main`:

```text
~/site (main) $ ls
index.html  style.css
~/site (main) $ git switch login
Switched to branch 'login'
~/site (login) $ ls
index.html  login.html  style.css
~/site (login) $ git switch -
Switched to branch 'main'
~/site (main) $ ls
index.html  style.css
```

The file isn't lost: it is in the `login` branch's commit. It comes back when
you switch back. `git switch -` returns to the previous branch (handy when
going back and forth between two branches).

## What about uncommitted changes?

Changes you haven't committed don't belong to a branch; they move with you.
Git reminds you of them when you switch (the `M` lines):

```text
~/site (main) $ echo "h1 {}" >> style.css
~/site (main) $ git switch -c contact
M       style.css
Switched to a new branch 'contact'
~/site (contact) $ git status -s
 M style.css
```

But if the same file is **different** on the branch you are going to, Git
refuses to switch so it doesn't overwrite your change:

```text
~/site (main) $ echo "<h1>Welcome</h1>" > index.html
~/site (main) $ git switch login
error: Your local changes to the following files would be overwritten by checkout:
        index.html
Please commit your changes or stash them before you switch branches.
Aborting
```

Two ways out: commit the change first, or put it aside (`git stash`, section
11).

## Managing branches

| Command | What it does |
|---|---|
| `git branch -m old new` | Renames a branch (`-m new` renames the one you are on). |
| `git branch -d name` | Deletes the branch; its work must be merged into another branch. |
| `git branch -D name` | **Force**-deletes the branch; unmerged commits drop off it. ⚠ |
| `git branch --merged` | Branches merged into the one you are on (safe to delete). |
| `git branch --no-merged` | Branches not merged yet. |

```text
~/site (main) $ git branch --merged
* main
  old-idea
~/site (main) $ git branch --no-merged
  experiment
  login
~/site (main) $ git branch -d old-idea
Deleted branch old-idea (was 7085b6f).
~/site (main) $ git branch -d experiment
error: the branch 'experiment' is not fully merged
hint: If you are sure you want to delete it, run 'git branch -D experiment'
hint: Disable this message with "git config set advice.forceDeleteBranch false"
~/site (main) $ git branch -D experiment
Deleted branch experiment (was 5d34b75).
~/site (main) $ git branch
  login
* main
```

`-d` refuses to delete an unmerged branch; it has commits that exist nowhere
else. If you really want to throw them away, use `-D`.

> You can't delete the branch you are on; switch to another branch first.

## Branch names

- Short and saying what it is for: `login`, `fix-typo`, `contact-page`.
- No spaces; separate words with `-`.
- Teams often use prefixes: `feature/login`, `fix/header`. The slash stores
  the branch as if it were in a folder; that is why `feature/login` can't be
  created while a branch named `feature` exists.
- In most projects the main branch is `main`. Instead of committing
  experiments to it directly, open a branch: let `main` always show the
  working version.

## Summary

- A branch is a movable name pointing to a commit; creating one is instant
  and cheap.
- `git branch` lists / creates, `git switch` switches, `git switch -c`
  creates and switches.
- A commit moves only the branch you are on; HEAD points to that branch.
- Switching branches brings the files to that branch's state; uncommitted
  changes move along, or Git refuses to switch.
- `git log --oneline --graph --all` draws the branches together.
- `-m` renames, `-d` deletes safely, `-D` force-deletes.
