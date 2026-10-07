# Overall Review

You've reached the end of the track. In this section we go over what you
learned once more through the life of a single project; then there is a
40-question mixed exam and five exercises that bring all the topics
together.

## The big picture

<figure class="fig">
  <div class="flow">
    <span class="node acc">branch</span><span class="arrow">→</span>
    <span class="node">commit</span><span class="arrow">→</span>
    <span class="node acc">PR</span><span class="arrow">→</span>
    <span class="node">merge</span><span class="arrow">→</span>
    <span class="node ok">tag</span>
  </div>
  <figcaption>The path of a piece of work: get the repo (or init), branch, commit, push and open a PR, merge, tag a release. git status at every step; when something goes wrong, 04 (undoing), 08 (conflicts) and 14 (recovery).</figcaption>
</figure>

| Topic | Section | Main commands |
|---|---|---|
| Repository and settings | 00–01 | `git init`, `git config --global` |
| Three areas, commit | 02 | `git status`, `git add`, `git commit -m` |
| Looking | 03 | `git diff`, `git log`, `git show`, `git blame` |
| Undoing | 04 | `git restore`, `--amend`, `git reset`, `git revert` |
| Ignoring | 05 | `.gitignore`, `git check-ignore` |
| Branches, merging, conflicts | 06–08 | `git switch -c`, `git merge`, `--abort` |
| Remotes, GitHub | 09–10 | `git clone`, `git push -u`, `git pull`, PR, fork |
| Putting aside | 11 | `git stash`, `git stash pop` |
| Rewriting history | 12 | `git rebase`, `git cherry-pick` |
| Releases | 13 | `git tag -a`, `git push --tags` |
| Recovery | 14 | `git reflog`, `HEAD@{n}` |
| Habits | 15 | small commits, good messages, GitHub Flow |

## The life of a project

Everything from a recipe site's first day to its first release, in one
session:

```text
~ $ mkdir recipes
~ $ cd recipes
~/recipes $ git init
Initialized empty Git repository in /home/ada/recipes/.git/
~/recipes (main) $ echo "__pycache__/" > .gitignore
~/recipes (main) $ echo "# Recipes" > README.md
~/recipes (main) $ git add .
~/recipes (main) $ git commit -m "Start recipe site"
[main (root-commit) 3c8e414] Start recipe site
 2 files changed, 2 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
~/recipes (main) $ git remote add origin https://github.com/ada/recipes.git
~/recipes (main) $ git push -u origin main
To https://github.com/ada/recipes.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
~/recipes (main) $ git switch -c soup
Switched to a new branch 'soup'
~/recipes (soup) $ echo "water" > soup.txt
~/recipes (soup) $ git add .
~/recipes (soup) $ git commit -m "Add soup recipe"
[soup 3123685] Add soup recipe
 1 file changed, 1 insertion(+)
 create mode 100644 soup.txt
~/recipes (soup) $ git push -u origin soup
remote: 
remote: Create a pull request for 'soup' on GitHub by visiting:
remote:      https://github.com/ada/recipes/pull/new/soup
remote: 
To https://github.com/ada/recipes.git
 * [new branch]      soup -> soup
branch 'soup' set up to track 'origin/soup'.
~/recipes (soup) $ git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
~/recipes (main) $ git merge --no-ff soup --no-edit
Merge made by the 'ort' strategy.
 soup.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 soup.txt
~/recipes (main) $ git branch -d soup
Deleted branch soup (was 3123685).
~/recipes (main) $ git push
To https://github.com/ada/recipes.git
   3c8e414..3c8d14a  main -> main
~/recipes (main) $ git tag -a v1.0 -m "First version"
~/recipes (main) $ git push origin v1.0
To https://github.com/ada/recipes.git
 * [new tag]         v1.0 -> v1.0
~/recipes (main) $ git log --oneline --graph
*   3c8d14a (HEAD -> main, tag: v1.0, origin/main) Merge branch 'soup'
|\  
| * 3123685 (origin/soup) Add soup recipe
|/  
* 3c8e414 Start recipe site
```

What happened in this session:

1. A repository was created, `.gitignore` written before the first commit.
2. The first push to the empty GitHub repository, with `-u`.
3. New work on a branch; the branch was pushed (a PR will be opened).
4. A merge with `--no-ff`; the branch was deleted.
5. The release was marked with an annotated tag, and the tag pushed
   separately.

## What do I do when…?

| Situation | Section | Way out |
|---|---|---|
| I don't understand what happened | all | `git status` |
| I want to throw away a change in a file | 04 | `git restore file` |
| I want to fix the last commit (not pushed) | 04 | `git commit --amend` |
| I want to undo a shared commit | 04 | `git revert` |
| Files I don't want show in `git status` | 05 | `.gitignore` |
| A conflict appeared | 08 | fix → `git add` → `git commit --no-edit` / `--abort` |
| The push was refused | 09 | `git pull`, then `git push` |
| I must switch branches with half-done work | 11 | `git stash` |
| My branch fell behind | 07 / 12 | `git merge main` or `git rebase main` |
| I lost something | 14 | `git reflog` |

## From here

You've learned the most used part of Git; most daily work runs on these
commands. The next step is **a real project**: create a repository on
GitHub and apply this track's flow to your own code. If you meet something
you don't know, the "From Here" note says where to look.
