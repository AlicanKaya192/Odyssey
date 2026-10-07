`.gitignore` patterns and what they match. When unsure, ask with
`git check-ignore -v <file>`.

| Pattern | Matches | Does not match |
|---|---|---|
| `*.log` | `a.log`, `logs/b.log` | `a.log.txt` |
| `debug.log` | `debug.log`, `src/debug.log` | `debug.logs` |
| `/debug.log` | `debug.log` (root only) | `src/debug.log` |
| `build/` | the `build/` folder and its contents, `src/build/` | a **file** named `build` |
| `build` | a `build` file **and** folder | — |
| `docs/*.pdf` | `docs/a.pdf` | `docs/x/a.pdf`, `a.pdf` |
| `**/cache/` | `cache/`, `src/cache/`, `a/b/cache/` | a file named `cache` |
| `data/raw/` | `data/raw/` and its contents | `raw/`, `src/data/raw/` |
| `!keep.log` | — (exception: `keep.log` is not ignored) | — |
| `*.csv` + `!sample.csv` | `big.csv` | `sample.csv` (exception) |

## Rules

1. Empty lines and lines starting with `#` are skipped.
2. Without a `/` in the pattern, the file name in every folder is checked.
3. With a `/` at the start or in the middle, the path is read relative to
   where the `.gitignore` is.
4. With a trailing `/`, folders only.
5. The last matching rule wins; an `!` exception goes below the general rule.
6. If a whole folder is ignored, no file inside can be rescued with `!`.
7. Only untracked files are affected; for a tracked file, `git rm --cached`.

## When something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| The file is in `.gitignore` but still shows as modified | It is already tracked. | `git rm --cached file` + commit |
| The `!` exception doesn't work | The whole folder is ignored, or the exception is **above** the rule. | Write `folder/*`; fix the order. |
| No rule works at all | The file got named `.gitignore.txt` (Windows hides the extension). | Check its name with `ls -a`. |
| I wanted to ignore a folder and a file went too | There was no trailing `/`. | Write `build/`. |
