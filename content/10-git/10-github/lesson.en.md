# Working with GitHub

Git was a tool; GitHub is a **workplace** built around that tool: where
repositories live online, where teams review code together, where bugs and
tasks are tracked. In this section we look at where GitHub meets Git:
creating a repository, **pull requests**, **forks** and **issues**.

> GitHub itself is a website; we'll describe the buttons to click. You'll do
> the terminal side (the part that is always the same) in the exercises.

## A repository page

A repository's page on GitHub has these tabs:

| Tab | What's there |
|---|---|
| **Code** | Files, branches, commit history; `README.md` rendered at the bottom. The green **Code** button gives the clone address. |
| **Issues** | Bug reports, requests, to-dos. |
| **Pull requests** | Branches waiting to be merged, and their discussion. |
| **Actions** | Automated jobs (like running the tests on every push). |
| **Settings** | Name, visibility, collaborators, branch protection. |

## Creating a repository

1. The **+** at the top right → **New repository**.
2. **Repository name**: short, no spaces (`notes`). **Description** is
   optional.
3. **Public** (everyone sees it) or **Private** (only you and those you
   invite).
4. If you already have a repository on your computer, **don't add a README,
   .gitignore or license**: keep the GitHub repository empty, otherwise the
   first push is refused (the two histories would start differently).
5. **Create repository**.

On the empty repository's page GitHub shows ready-made commands. The "create
a new repository on the command line" part is:

```text
~/notes $ echo "# notes" >> README.md
~/notes $ git init
Initialized empty Git repository in /home/ada/notes/.git/
~/notes (main) $ git add README.md
~/notes (main) $ git commit -m "first commit"
[main (root-commit) 9a20964] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
~/notes (main) $ git branch -M main
~/notes (main) $ git remote add origin https://github.com/ada/notes.git
~/notes (main) $ git push -u origin main
To https://github.com/ada/notes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

The only new command is `git branch -M main`: it force-renames the branch you
are on to `main` (for repositories created with older settings as
`master`). The branch is already `main` here, so nothing changed.

## README.md

The file rendered on the repository's home page is `README.md`. It is what
someone seeing the project for the first time reads: what it does, how to
install it, how to use it. It is written in Markdown:

```text
# My notes

A small repository where I track my daily jobs.

## Usage

- `todo.txt` things to do
- `done.txt` things done
```

`#` is a heading, `-` a list item, backticks code. GitHub shows them
formatted.

## Pull request: "would you merge my branch?"

In teams nobody pushes straight to `main` (the feature branch workflow from
07). Instead the branch is pushed to GitHub and a **pull request** (PR) is
opened: "I want to merge this branch into `main`, would you take a look?"

<figure class="fig">
  <div class="flow">
    <span class="node">Branch + push</span><span class="arrow">→</span>
    <span class="node">Open a PR</span><span class="arrow">→</span>
    <span class="node">Review</span><span class="arrow">→</span>
    <span class="node ok">Merge</span><span class="arrow">→</span>
    <span class="node acc">git pull</span>
  </div>
  <figcaption>The life of a pull request. Changes requested in review are pushed to the same branch; the PR updates itself.</figcaption>
</figure>

### 1. Push the branch

```text
~/site (main) $ git switch -c contact-form
Switched to a new branch 'contact-form'
~/site (contact-form) $ echo "<form>" > contact.html
~/site (contact-form) $ git add .
~/site (contact-form) $ git commit -m "Add contact form"
[contact-form 94887a5] Add contact form
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (contact-form) $ git push -u origin contact-form
remote: 
remote: Create a pull request for 'contact-form' on GitHub by visiting:
remote:      https://github.com/ada/site/pull/new/contact-form
remote: 
To https://github.com/ada/site.git
 * [new branch]      contact-form -> contact-form
branch 'contact-form' set up to track 'origin/contact-form'.
```

When GitHub sees the new branch, it gives the link to open a PR in the
`remote:` lines. A yellow **Compare & pull request** bar also appears on the
repository page.

### 2. Open the PR

On the page that opens: which branch into which (`base: main` ←
`compare: contact-form`), a title and a description (what changed, why, how
to try it). **Create pull request**.

### 3. Review

Your teammates see the diff line by line in the **Files changed** tab, comment
on lines, and choose **Approve** or **Request changes**. If changes are
requested, you commit and push on the same branch; the PR updates itself. No
new PR is opened.

### 4. Merging

After approval, **Merge pull request** on GitHub. There are three options:

| Option | What it does |
|---|---|
| **Create a merge commit** | Like `--no-ff`: the branch's commits + a merge commit. |
| **Squash and merge** | All the branch's commits are squashed into one commit. |
| **Rebase and merge** | The branch's commits are replayed one by one on the tip of `main` (12). |

Then GitHub offers to delete the branch (**Delete branch**).

### 5. Update your own computer

The merge happened on GitHub; your computer doesn't know. Tidying up the
local side:

```text
~/site (contact-form) $ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
~/site (main) $ git pull
From https://github.com/ada/site
   05e1329..312cf67  main       -> origin/main
Updating 05e1329..312cf67
Fast-forward
 contact.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 contact.html
~/site (main) $ git branch -d contact-form
Deleted branch contact-form (was 94887a5).
~/site (main) $ git fetch --prune
From https://github.com/ada/site
 - [deleted]         (none)     -> origin/contact-form
~/site (main) $ git log --format="%h %s" -3
312cf67 Merge pull request #1 from ada/contact-form
94887a5 Add contact form
05e1329 Add home page
~/site (main) $ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
```

- `git switch main` + `git pull`: take the merged `main`.
- `git branch -d`: delete the local branch (its work is on `main` now).
- `git fetch --prune`: remove the `origin/...` traces of branches deleted on
  GitHub.

> If **Squash and merge** was used, your branch's commits are **not** in
> `main` as they were (a single new commit replaced them). That's why
> `git branch -d` says "not fully merged"; if the work really was merged,
> delete it with `-D`.

## Fork: contributing to someone else's project

You can't push to a repository you have no write access to (like an open
source project). Instead you **fork**: the **Fork** button on the repository
page creates a copy, with all its history, **in your own account**.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>upstream</span><span>github.com/grace/site — the original repository. You can read it, not write to it.</span></div>
    <div class="anat-row"><span>origin</span><span>github.com/ada/site — your fork. You push here.</span></div>
    <div class="anat-row"><span>Your computer</span><span>A clone of origin. You take updates from upstream and send your work to origin.</span></div>
  </div>
  <figcaption>The fork flow has two remotes. The PR goes from a branch on your fork to the original repository.</figcaption>
</figure>

The flow:

1. Fork the original repository → `github.com/ada/site`.
2. Clone **your own fork** (it becomes `origin`).
3. Add the original as `upstream`: you'll take updates from there.
4. Create a branch, work, push to your fork.
5. On GitHub, open a PR from your fork to the original repository.

Keeping the fork up to date:

```text
~/site (main) $ git remote add upstream https://github.com/grace/site.git
~/site (main) $ git remote -v
origin  https://github.com/ada/site.git (fetch)
origin  https://github.com/ada/site.git (push)
upstream        https://github.com/grace/site.git (fetch)
upstream        https://github.com/grace/site.git (push)
~/site (main) $ git fetch upstream
From https://github.com/grace/site
 * [new branch]      main       -> upstream/main
~/site (main) $ git merge upstream/main
Updating 7446ff5..c1276e9
Fast-forward
 news.html | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 news.html
~/site (main) $ git push
To https://github.com/ada/site.git
   7446ff5..c1276e9  main -> main
```

## Issues

An **issue** is a bug report, a request or a to-do. Every issue has a number
(`#12`). If you write `Fixes #12` in a commit message or a PR description,
the issue closes itself when the PR is merged. PRs and issues share the same
number sequence.

## A few settings and tools

- **Collaborators** (Settings): people you give write access to.
- **Branch protection**: blocks direct pushes to `main`, requires a PR and
  approval.
- **GitHub Desktop** and **VS Code**'s Git panel do everything in this section
  with buttons; the same commands run underneath.
- **`gh`**: GitHub's command-line tool (`gh pr create`, `gh repo clone`);
  installed separately.

## Summary

- Create an empty repository on GitHub; don't add a README if you'll push an
  existing repository.
- Pull request: push the branch → open a PR → review → merge → locally
  `pull`, `branch -d`, `fetch --prune`.
- Use `-D` to delete a squashed branch.
- Fork: your copy (`origin`) + the original (`upstream`); to update,
  `fetch upstream`, `merge upstream/main`, `push`.
- `Fixes #12` closes the issue when the PR is merged.
