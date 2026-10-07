When a conflict shows up, in order.

## 1. Stay calm, look

```text
git status
```

Every file under `Unmerged paths` is waiting to be resolved. The prompt says
`MERGING`. If you don't understand what happened:

```text
git merge --abort
```

puts everything back to before the merge. Nothing is lost.

## 2. Resolve each file

Open the file and find the markers:

```text
<<<<<<< HEAD
the line on our branch
=======
the line on the branch we are bringing in
>>>>>>> summer
```

Leave the right version and delete the three marker lines. Make sure no
`<<<<<<<` is left in the file.

To take one side as it is:

| What do you want? | Command |
|---|---|
| Our branch's version | `git checkout --ours file` |
| The incoming branch's version | `git checkout --theirs file` |

## 3. Mark it

```text
git add file
```

For each conflicted file. `git status` now says `All conflicts fixed but you
are still merging`.

## 4. Finish

```text
git commit --no-edit
```

or `git merge --continue`. In a real terminal, without `--no-edit` Git opens
an editor for the message; saving the ready-made message and closing is
enough.

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Committing is not possible because you have unmerged files` | You didn't mark the conflicted file with `git add`. | `git add file` |
| The code breaks, the file contains `<<<<<<<` | You ran `git add` without deleting the markers. | Fix the file, `git add` again, `git commit --amend --no-edit`. |
| `You have not concluded your merge` | A new `git merge` while a merge is unfinished. | Finish it first, or `--abort`. |
| `There is no merge to abort` | No merge is in progress. | Look with `git status`. |
