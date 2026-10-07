# Good Habits

You know Git's commands now. This section is less about commands and more
about **how they are used**: commits that keep history readable, good
messages, teams' branching patterns and a few settings that speed you up.
These aren't rules but habits teams arrived at over the years; they make
life easier for everyone reading the history (most of all, you in a few
months).

## Small, single-purpose commits

A good commit tells **one thing** and makes sense on its own.

| Bad | Good |
|---|---|
| "Today's work": a typo fix + a new feature + a formatting change | Three separate commits |
| A week of work in one commit | A commit at each logical step |
| Half-done, broken code on `main` | Half-done work on a branch; `main` always works |

Why?

- It's easy to find **which change** brought in a bug.
- **Undoing** one change (`git revert`) doesn't break the others.
- A reviewer understands what you did and why.

Before committing, look at what goes in with `git diff --staged` (03); if
there are two jobs, split them with `git add file` (02).

## The commit message

<figure class="fig">
  <pre><code class="language-text">Fix crash when the cart is empty

The total was divided by the item count, which is
zero for an empty cart. Return 0 instead.</code></pre>
  <div class="anat">
    <div class="anat-row"><span>Subject</span><span>Short (≤ 50 characters), imperative, no full stop. git log --oneline shows this.</span></div>
    <div class="anat-row"><span>Blank line</span><span>Separates the subject from the body.</span></div>
    <div class="anat-row"><span>Body</span><span>Why was it done? The diff already shows what.</span></div>
  </div>
  <figcaption>The three parts of a good commit message.</figcaption>
</figure>

Rules:

1. **A short subject** (about 50 characters), no full stop at the end.
2. **Imperative mood**: `Add`, `Fix`, `Remove`, `Update`, `Rename`. It
   completes the sentence "If applied, this commit will…": *…Add search box*.
3. If needed, **a body after a blank line**: not what changed (the diff shows
   that), but **why** it changed.

In the terminal, for two paragraphs you write `-m` twice:

```text
~/site (main) $ echo "<h1>Home</h1>" > index.html
~/site (main) $ git commit -am "Fix title typo" -m "Visitors reported it."
[main b88cfa3] Fix title typo
 1 file changed, 1 insertion(+), 1 deletion(-)
~/site (main) $ git log -1
commit b88cfa3ac7cde15a179e77f0116e09a7d444d042 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Fix title typo
    
    Visitors reported it.
~/site (main) $ git log --oneline
b88cfa3 (HEAD -> main) Fix title typo
772525a Add home page
```

| Bad message | Why it's bad | Better |
|---|---|---|
| `fix` | Fix what? | `Fix crash when the cart is empty` |
| `update index.html` | The diff already says the file name | `Add opening hours to the home page` |
| `asdf`, `wip`, `.` | Says nothing | (squash or reword it) |
| `Fixed bugs and added stuff` | Two jobs, vague | Two commits, two clear subjects |

## Conventional Commits (optional)

Some teams put the type at the start of the subject; tools generate release
notes from it:

| Prefix | Meaning |
|---|---|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `docs:` | Documentation only |
| `refactor:` | A code change that doesn't change behaviour |
| `test:` | Tests |
| `chore:` | Maintenance (dependencies, settings) |

Example: `feat: add dark mode`, `fix: handle empty cart`. Follow it if your
team uses it; otherwise it isn't required.

## Branching patterns

| Pattern | How | Who it suits |
|---|---|---|
| **GitHub Flow** | `main` + short-lived feature branches + PRs | Most projects, continuous releases |
| **Git Flow** | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` | Products released on set dates |
| **Trunk-based** | Everyone commits very often, in very small commits, straight to `main` (with feature flags) | Teams with strong automated tests |

If you don't know, start with **GitHub Flow**: everything in this track
follows it.

## The daily flow

```text
git switch main && git pull           an up-to-date main
git switch -c add-faq                 a branch for the work
... small commits ...
git push -u origin add-faq            push, open a PR
... review, merge ...
git switch main && git pull           the merged main
git branch -d add-faq                 tidy up
```

## Time-saving settings

| Setting | What it does |
|---|---|
| `git config --global alias.lg "log --oneline --graph --all"` | A `git lg` shortcut. |
| `git config --global alias.st "status -s"` | `git st`. |
| `git config --global pull.rebase true` | `pull` replays local commits on top of incoming ones (12). |
| `git config --global fetch.prune true` | Every fetch removes deleted remote branches. |
| `git config --global push.autoSetupRemote true` | No need for `-u origin branch` on a new branch's first `git push`. |

A shortcut is defined once and then used like a command:

```text
~/site (main) $ git config --global alias.lg "log --oneline --graph --all"
~/site (main) $ git lg
* 772525a (HEAD -> main) Add home page
~/site (main) $ git config --global alias.st "status -s"
~/site (main) $ echo "x" >> index.html
~/site (main) $ git st
 M index.html
```

## When you mistype

Git suggests the closest command when you mistype one; read the message:

```text
~/site (main) $ git comit
git: 'comit' is not a git command. See 'git --help'.

The most similar command is
        commit
~/site (main) $ git stauts
git: 'stauts' is not a git command. See 'git --help'.

The most similar command is
        status
```

If you forget a command's options, in a real terminal `git <command> -h` gives
short help and `git help <command>` long help.

## And also

- **Never commit secrets**, and write `.gitignore` before the first commit
  (05).
- **Don't rewrite shared history** (12): `--amend`, `rebase` and `reset` only
  on commits that are only yours.
- **Push often.** A commit that is only on your computer isn't backed up.
- **`git status` first.** The most important habit of this track since day
  one.

## Summary

- A commit is small, single-purpose and meaningful on its own.
- Message: a short, imperative subject; if needed, "why" after a blank line.
- Conventional Commits is an option (`feat:`, `fix:`).
- If you don't know a branching pattern, GitHub Flow.
- Shortcuts and settings like `pull.rebase`, `fetch.prune` and
  `push.autoSetupRemote` save time.
