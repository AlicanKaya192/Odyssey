The commands for "what happened?". None of them changes anything.

## What changed?

| Question | Command |
|---|---|
| Which files changed? | `git status` / `git status -s` |
| What haven't I staged yet? | `git diff` |
| What goes into the commit? | `git diff --staged` |
| Everything since the last commit? | `git diff HEAD` |
| Only one file? | `git diff -- file` |
| Just a summary | `git diff --stat` / `--name-only` |

## History

| Question | Command |
|---|---|
| Recent commits | `git log --oneline -10` |
| Which files changed? | `git log --stat` |
| With full diffs | `git log -p` |
| Who touched this file, and when? | `git log --oneline -- file` |
| What did Grace do? | `git log --author=Grace` |
| Messages containing "fix" | `git log --grep=fix -i` |
| In my own layout | `git log --format="%h %an %s"` |

## One commit, or an old version of a file

| Question | Command |
|---|---|
| What changed in the last commit? | `git show` |
| Which files in this commit? | `git show --stat <commit>` |
| What did the file look like two commits ago? | `git show HEAD~2:file` |
| What changed between two commits? | `git diff <old> <new>` |
| Who wrote this line, in which commit? | `git blame file` |

## Reading diff output

```text
diff --git a/todo.txt b/todo.txt     which file
index ab0af58..254c209 100644        ids of the old and new content
--- a/todo.txt                       old version
+++ b/todo.txt                       new version
@@ -1,2 +1,3 @@                      old: 2 lines from line 1, new: 3 lines from line 1
 Buy milk                            unchanged
 Call Ada                            unchanged
+Buy bread                           added
```

A line starting with `-` was removed, one starting with `+` was added. A
changed line shows up as one `-` and one `+`.
