# Conflicts

When Git merges two branches it usually handles everything itself. But if
both branches changed **the same line of the same file differently**, it
can't know which is right. Then it stops the merge halfway and leaves the
decision to you: that is a **merge conflict**.

A conflict is not an error; it is a **question**. Nothing to be afraid of
either: if you don't know what to do, one command cancels the merge.

## First: what does Git merge by itself?

A shop's intro page (`page.txt`) has three lines. Say the first line changed
on the `summer` branch and the last line on `main`: different lines, no
conflict.

```text
~/shop (main) $ git merge summer --no-edit
Auto-merging page.txt
Merge made by the 'ort' strategy.
 page.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
~/shop (main) $ cat page.txt
Welcome to summer!
We sell books
Open 8-17
```

`Auto-merging page.txt` says Git looked inside the file and took both
changes.

## What does a conflict look like?

Now say both branches changed **the same line** (the opening hours)
differently: `Open 9-20` on `summer`, `Open 8-17` on `main`.

```text
~/shop (main) $ git merge summer
Auto-merging page.txt
CONFLICT (content): Merge conflict in page.txt
Automatic merge failed; fix conflicts and then commit the result.
~/shop (main|MERGING) $ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   page.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Three things happened:

1. Git said `CONFLICT` and wrote which file it is in.
2. The merge **stopped halfway**: no commit was made. The prompt became
   `(main|MERGING)`; it says "you are in the middle of a merge".
3. `git status` shows the conflicted file under **Unmerged paths** as `both
   modified`.

## Conflict markers

Git wrote both versions into the conflicted file:

```text
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
<<<<<<< HEAD
Open 8-17
=======
Open 9-20
>>>>>>> summer
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</span><span>Where our side starts: the branch you are on (main).</span></div>
    <div class="anat-row"><span>Open 8-17</span><span>The version on main.</span></div>
    <div class="anat-row"><span>=======</span><span>The line separating the two sides.</span></div>
    <div class="anat-row"><span>Open 9-20</span><span>The version on the branch you are bringing in.</span></div>
    <div class="anat-row"><span>&gt;&gt;&gt;&gt;&gt;&gt;&gt; summer</span><span>Where the incoming side ends, with the branch name.</span></div>
  </div>
  <figcaption>Resolving: replace these five lines with the right line (or lines) and delete the markers.</figcaption>
</figure>

`HEAD` is the branch you are on (`main`), `summer` is the branch you are
bringing in. Git was only confused about that line; the rest of the file
(`Welcome`, `We sell books`) is normal.

## Resolving: three steps

1. **Bring the file to the final version you want.** Delete the marker lines
   (`<<<<<<<`, `=======`, `>>>>>>>`) and leave the right content. It can be
   one side, the other, or a mix; your call. Here let's decide to open at 8 in
   the morning and close at 8 in the evening: `Open 8-20`.
2. **`git add file`** says "I resolved this file".
3. **Finish the merge:** `git commit --no-edit` (with the ready-made merge
   message). `git merge --continue` does the same.

```text
~/shop (main|MERGING) $ echo "Welcome" > page.txt
~/shop (main|MERGING) $ echo "We sell books" >> page.txt
~/shop (main|MERGING) $ echo "Open 8-20" >> page.txt
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
Open 8-20
~/shop (main|MERGING) $ git add page.txt
~/shop (main|MERGING) $ git status
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

Changes to be committed:
        modified:   page.txt
~/shop (main|MERGING) $ git commit --no-edit
[main c02108b] Merge branch 'summer'
~/shop (main) $ git log --oneline --graph
*   c02108b (HEAD -> main) Merge branch 'summer'
|\  
| * 524d5b4 (summer) Summer hours
* | 41667c0 Open earlier
|/  
* 071cfb3 Add page
```

> In a real project you open the file in an editor and fix it. VS Code
> recognises conflict markers and shows *Accept Current Change* (ours),
> *Accept Incoming Change* (theirs) and *Accept Both Changes* links above
> them. Odyssey's terminal has no editor, so we rewrite the file with `echo`:
> the first line with `>`, the rest with `>>`.

## Taking one side as it is

Sometimes the answer is simple: "entirely mine" or "entirely theirs".
Instead of editing line by line:

| Command | The file goes back to |
|---|---|
| `git checkout --ours file` | The version on the branch you are on (`HEAD`). |
| `git checkout --theirs file` | The version on the branch you are merging. |

(`git restore --ours` / `--theirs` do the same.) Then `git add` and commit
as usual:

```text
~/shop (main|MERGING) $ git checkout --theirs page.txt
Updated 1 path from the index
~/shop (main|MERGING) $ cat page.txt
Welcome
We sell books
Open 9-20
~/shop (main|MERGING) $ git add page.txt
~/shop (main|MERGING) $ git commit -m "Merge summer hours"
[main 1f9b310] Merge summer hours
```

> In a merge, **ours** is always the branch you are on and **theirs** the
> branch you passed to `git merge`. (In `rebase`, which we'll see in 12, they
> swap; that is why people mix them up.)

## Backing out: `git merge --abort`

If the conflict is bigger than expected, or you merged the wrong branch,
cancel the merge. Everything goes back to how it was before `git merge`:

```text
~/shop (main) $ git merge summer
Auto-merging page.txt
CONFLICT (content): Merge conflict in page.txt
Automatic merge failed; fix conflicts and then commit the result.
~/shop (main|MERGING) $ git merge --abort
~/shop (main) $ git status
On branch main
nothing to commit, working tree clean
~/shop (main) $ cat page.txt
Welcome
We sell books
Open 8-17
```

## You can't commit before resolving

If you try to commit without marking the conflicted file with `git add`, Git
refuses and tells you which files are waiting:

```text
~/shop (main|MERGING) $ git commit -m "Merge"
error: Committing is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
U       page.txt
```

## Fewer conflicts

- **Small, frequent commits; short-lived branches.** The longer a branch
  lives, the more it drifts from `main`.
- **Merge `main` into your branch often** (07). Conflicts are resolved while
  they are small.
- **Talk if you'll work on the same file.** That's the team's job, not
  Git's.
- **Don't mix in reformatting.** Changing the indentation of a whole file
  makes every line "changed"; it will clash with someone else's work.

## Summary

- A conflict: both branches changed the same line differently; Git asks.
- `git status` shows conflicted files as `both modified`; the prompt says
  `MERGING`.
- Markers: `<<<<<<< HEAD` (ours) … `=======` … `>>>>>>> branch` (theirs).
- Resolving: fix the file → `git add` → `git commit --no-edit`.
- `--ours` / `--theirs` take one side as it is.
- `git merge --abort` puts everything back to before the merge.
