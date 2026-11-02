The most used forms of find, at a glance.

## Structure

```text
find  <where from>  <conditions>  <action>
```

Where from: one or more paths (`.` is the current folder). Conditions: all
must hold. Action: without one, it prints the paths.

## Conditions

| Condition | What it selects |
|---|---|
| `-name '*.py'` | Names that fit the pattern (case sensitive) |
| `-iname '*.md'` | The same, ignoring upper/lower case |
| `-type f` | Files |
| `-type d` | Folders |
| `-maxdepth 1` | At most this depth |
| `-mindepth 1` | At least this depth (the start folder is left out) |
| `-not -name 'p'` / `! -name 'p'` | Those that do not fit |

In a real terminal also: `-size +1M`, `-mtime -7`, `-empty`, and `-o` for "or".

## Actions

| Action | What it does |
|---|---|
| (none) | Prints the paths |
| `-exec command {} \;` | Runs the command for each match |
| `-delete` | Deletes the matches, without asking |

## Common patterns

- Every Python file: `find . -name '*.py'`
- How many: `find . -name '*.py' | wc -l`
- Every folder, empty ones included: `find . -type d`
- Files containing a word: `find . -name '*.py' -exec grep -l TODO {} \;`
- Only this folder: `find . -maxdepth 1 -type f`
