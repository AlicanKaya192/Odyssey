# Remote Repositories

So far everything lived only on your computer. If the computer breaks, the
history goes with it; working with others isn't possible either. A
**remote** is a copy of the same repository somewhere else: usually on
GitHub.

You do three things with a remote:

- **`clone`**: download the remote repository with its history.
- **`push`**: send your commits to the remote.
- **`fetch` / `pull`**: get the commits others have sent.

<figure class="fig">
  <div class="flow">
    <span class="node">You<br><small>main</small></span><span class="arrow">→</span>
    <span class="node acc">git push</span><span class="arrow">→</span>
    <span class="node ok">GitHub<br><small>origin</small></span><span class="arrow">→</span>
    <span class="node acc">git pull</span><span class="arrow">→</span>
    <span class="node">A teammate<br><small>main</small></span>
  </div>
  <figcaption>GitHub is the common meeting point: everyone sends their commits there and takes others' from there.</figcaption>
</figure>

> This section's terminal imitates GitHub: the `https://github.com/...`
> addresses live inside the simulator, nothing goes to the internet. The
> commands and output are the same as with real GitHub; only the download
> progress lines (like `Receiving objects: 100%`) are left out.

## `git clone`: downloading

Let's download Grace's recipe repository:

```text
~ $ git clone https://github.com/grace/recipes.git
Cloning into 'recipes'...
~ $ cd recipes
~/recipes (main) $ ls
README.md  soup.txt
~/recipes (main) $ git log --oneline
b2024e6 (HEAD -> main, origin/main, origin/HEAD) Add soup
~/recipes (main) $ git remote -v
origin  https://github.com/grace/recipes.git (fetch)
origin  https://github.com/grace/recipes.git (push)
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`git clone` did four things:

1. It created the `recipes` folder and downloaded every commit.
2. It saved the remote under the name **`origin`** (`git remote -v`).
   `origin` is just a nickname meaning "where I downloaded from".
3. For each remote branch it created a **remote-tracking branch**:
   `origin/main`.
4. It set your `main` branch to **track** `origin/main`; that is why
   `git status` says "up to date with 'origin/main'".

## Remote-tracking branches

`origin/main` means "**the last time I looked**, `main` on GitHub was here". It
lives on your computer and does not update by itself; only `fetch`, `pull`
and `push` update it. So before Git can tell you "you are behind", it has to
look at GitHub (`fetch`).

| Name | What |
|---|---|
| `main` | Your branch; it moves when you commit. |
| `origin/main` | The last known position of `main` on GitHub. |
| `origin/HEAD` | The remote's default branch (points to `origin/main`). |

## `git push`: sending

Let's make a change and send it:

```text
~/recipes (main) $ echo "salt" >> soup.txt
~/recipes (main) $ git commit -am "Add salt"
[main d7bf1c2] Add salt
 1 file changed, 1 insertion(+)
~/recipes (main) $ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
   b2024e6..d7bf1c2  main -> main
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

After the commit, `git status` says "ahead of 'origin/main' by 1 commit":
you have it, GitHub doesn't. `git push` sent it; the last line `old..new  main
-> main` means "I moved main on GitHub from this commit to that one".

## Putting your own repository on GitHub

To send a repository you started with `git init` for the first time:

1. Create an **empty** repository on GitHub (without a README; step by step
   in 10). GitHub gives you its address.
2. Save the address under the name `origin`: `git remote add origin
   <url>`.
3. Do the first push with `-u`: `git push -u origin main`.

```text
~/notes (main) $ git remote add origin https://github.com/ada/notes.git
~/notes (main) $ git remote -v
origin  https://github.com/ada/notes.git (fetch)
origin  https://github.com/ada/notes.git (push)
~/notes (main) $ git push -u origin main
To https://github.com/ada/notes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
~/notes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

`-u` (*set upstream*) says "from now on, `main` tracks `origin/main`". After
doing it once, you just type `git push` and `git pull`.

> **On the first push to real GitHub** you have to prove who you are. On
> Windows, the *Git Credential Manager* that comes with Git opens GitHub's
> sign-in page in the browser; you approve once and it is remembered. GitHub
> no longer accepts pushes with your account password; you need the browser
> sign-in, a personal access token, or an SSH key.

If the address is wrong, or the repository wasn't created on GitHub:

```text
~/notes (main) $ git remote add origin https://github.com/ada/notse.git
~/notes (main) $ git push -u origin main
remote: Repository not found.
fatal: repository 'https://github.com/ada/notse.git/' not found
```

## `git fetch`: looking

Say Grace sent a new commit to the repository. Your computer doesn't know;
you have to ask first:

```text
~/recipes (main) $ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
~/recipes (main) $ git fetch
From https://github.com/grace/recipes
   b2024e6..37e19db  main       -> origin/main
~/recipes (main) $ git status
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
~/recipes (main) $ git log --oneline --all
37e19db (origin/main, origin/HEAD) Add bread recipe
b2024e6 (HEAD -> main) Add soup
~/recipes (main) $ ls
README.md  soup.txt
```

`git fetch` downloaded the new commits and moved `origin/main`; **it didn't
touch your `main` branch**, your files didn't change. Now `git status` can
tell you that you are behind. `fetch` is safe: it changes nothing of yours,
it only brings news.

## `git pull`: taking

`git pull` = `git fetch` + `git merge origin/main`. If you have no new commits,
the merge is a fast-forward:

```text
~/recipes (main) $ git pull
From https://github.com/grace/recipes
   b2024e6..37e19db  main       -> origin/main
Updating b2024e6..37e19db
Fast-forward
 bread.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 bread.txt
~/recipes (main) $ ls
README.md  bread.txt  soup.txt
```

## If both sides moved

You made a commit, and meanwhile Grace pushed too. When you try to push:

```text
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/grace/recipes.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

GitHub refused: accepting would have lost Grace's commit. You must take her
work first. But `git pull` also wants a decision:

```text
~/recipes (main) $ git status
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
~/recipes (main) $ git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

Because the two branches diverged, Git asks whether you want a merge or a
rebase (12). Let's choose merge; to avoid typing it every time, you can set
it once: `git config --global pull.rebase false`.

```text
~/recipes (main) $ git pull --no-rebase --no-edit
From https://github.com/grace/recipes
   b2024e6..458d82a  main       -> origin/main
Merge made by the 'ort' strategy.
 bread.txt | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 bread.txt
~/recipes (main) $ git log --oneline --graph
*   dd028b4 (HEAD -> main) Merge branch 'main' of https://github.com/grace/recipes
|\  
| * 458d82a (origin/main, origin/HEAD) Add bread recipe
* | d7bf1c2 Add salt
|/  
* b2024e6 Add soup
~/recipes (main) $ git push
To https://github.com/grace/recipes.git
   458d82a..dd028b4  main -> main
```

Now your commits and Grace's are combined; the push is accepted.

## Pushing branches

You can push your own branch too; teammates see it and you open a pull
request on GitHub (10):

```text
~/recipes (main) $ git switch -c spicy
Switched to a new branch 'spicy'
~/recipes (spicy) $ echo "chili" >> soup.txt
~/recipes (spicy) $ git commit -am "Add chili"
[spicy cf97db7] Add chili
 1 file changed, 1 insertion(+)
~/recipes (spicy) $ git push
fatal: The current branch spicy has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin spicy

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

~/recipes (spicy) $ git push -u origin spicy
remote: 
remote: Create a pull request for 'spicy' on GitHub by visiting:
remote:      https://github.com/grace/recipes/pull/new/spicy
remote: 
To https://github.com/grace/recipes.git
 * [new branch]      spicy -> spicy
branch 'spicy' set up to track 'origin/spicy'.
~/recipes (spicy) $ git branch -a
  main
* spicy
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
  remotes/origin/spicy
```

The lines starting with `remote:` are written by GitHub: it gives a "pull
request" link for the new branch. We'll see pull requests in the next section.

To delete a branch on GitHub: `git push origin --delete branch`.

## Don't change pushed history

`--amend`, `reset` and `rebase` rewrite history. That's fine while the
commits are only yours. If you do it **after pushing**, your history and the
one on GitHub split apart and `push` is refused. `git push --force` pushes
over the refusal but **deletes** commits others pushed in the meantime. ⚠
Don't force-push a shared branch; if you must, at least use
`--force-with-lease` (it refuses if someone else pushed).

## Summary

- A remote is a copy elsewhere; its default name is `origin`.
- `git clone` downloads and sets up `origin` and tracking.
- `origin/main` is the last known position of the branch on GitHub; `fetch`
  / `pull` / `push` update it.
- `git push` sends; the first time, `git remote add origin <url>` +
  `git push -u origin main`.
- `git fetch` only brings news; `git pull` = fetch + merge.
- A refused push: first `git pull` (with `--no-rebase` if needed), then
  `git push`.
- Don't rewrite shared history; don't force-push.
