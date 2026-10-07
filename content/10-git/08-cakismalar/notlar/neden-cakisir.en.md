Git looks at lines, not meaning. Knowing when it merges by itself and when it
asks lets you see conflicts coming.

| What did the two branches do? | Result |
|---|---|
| Changed different files | Merges by itself. |
| Changed distant lines of the same file | Merges by itself (`Auto-merging`). |
| Changed the same line the same way | Merges by itself; the change is written once. |
| Changed the same line differently | **Conflict** (`CONFLICT (content)`). |
| Changed adjacent lines | Usually a **conflict**; Git can't tell where one ends. |
| One deleted the file, the other changed it | **Conflict** (`CONFLICT (modify/delete)`). |
| Both added a new file with the same name, different content | **Conflict** (`CONFLICT (add/add)`). |

## Git doesn't know meaning

A merge without conflicts doesn't always mean a **correct** result. For
example, one branch renamed a function and the other called it by its old
name somewhere new: different lines, Git merges happily, but the program
breaks. That is why you run the program and its tests after merging; teams
use tools that do this automatically (*CI*).

## Not resolving the same conflict twice

If you merge `main` into a long-lived branch often, the same conflict can
come back again and again. Git's `rerere` (*reuse recorded resolution*)
setting remembers a conflict you resolved once and applies it by itself next
time:

```text
git config --global rerere.enabled true
```

Not needed to start; useful in growing projects.
