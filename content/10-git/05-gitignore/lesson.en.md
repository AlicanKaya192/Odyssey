# .gitignore: Ignoring Files

Every project has files Git should **never** track:

- Files the program produces itself: `__pycache__/`, `build/`, `.log`
  files. They can be rebuilt from the source code; they take up space in the
  repository and show as "changed" after every run.
- Personal or secret files: `.env` with passwords and keys, the editor's
  settings folder, the virtual environment (`.venv/`).
- Big data files: `.csv` files of hundreds of MB, model files.

They show up as `??` in `git status` every time and can slip into a commit
with `git add .`. The fix: a text file named **`.gitignore`** at the root of
the repository. Each line is a **pattern**; Git ignores the files that match
it.

## Before and after

In a Python project without a `.gitignore`:

```text
~/app (main) $ git status -s
?? .env
?? __pycache__/
?? app.py
?? build/
?? debug.log
?? error.log
```

Only one of the six lines (`app.py`) is really our code. Let's write a
`.gitignore`:

```text
~/app (main) $ echo "*.log" > .gitignore
~/app (main) $ echo "build/" >> .gitignore
~/app (main) $ echo ".env" >> .gitignore
~/app (main) $ echo "__pycache__/" >> .gitignore
~/app (main) $ cat .gitignore
*.log
build/
.env
__pycache__/
~/app (main) $ git status -s
?? .gitignore
?? app.py
~/app (main) $ git status -s --ignored
?? .gitignore
?? app.py
!! .env
!! __pycache__/
!! build/
!! debug.log
!! error.log
```

Now `git status` shows only what should be tracked. The ignored files are
not gone; they are still in the folder and show up with `--ignored` (marked
`!!`).

**The `.gitignore` itself is committed.** That way everyone who gets the
repository uses the same rules.

## Patterns

| Pattern | Matches |
|---|---|
| `debug.log` | A file with this name in any folder. |
| `*.log` | Any file ending in `.log` (`*` means "anything"). |
| `build/` | **Folders** named `build` and everything inside. |
| `/todo.txt` | Only the `todo.txt` **at the root** (a leading `/` means "start here"). |
| `docs/*.pdf` | Only the `.pdf` files in the `docs` folder. |
| `**/cache/` | `cache` folders at any depth. |
| `!keep.log` | **Exception:** don't ignore this, even if a rule above catches it. |
| `# note` | A comment. |

Two details:

- With a trailing `/` the pattern matches **folders only**. `build/` does
  not catch a file named `build`; `build` catches both.
- Rules are read in order and **the last one wins**. That is why an `!`
  exception goes **below** the general rule.

```text
~/app (main) $ git status -s
?? .gitignore
?? app.py
~/app (main) $ echo '!keep.log' >> .gitignore
~/app (main) $ git status -s
?? .gitignore
?? app.py
?? keep.log
```

In the terminal, write a line containing `!` in **single quotes**:
`echo '!keep.log' >> .gitignore`. Bash reads `!` inside double quotes as a
reference to earlier commands and fails with `event not found`.

> If a whole folder is ignored, you can't bring back a file inside it with
> `!`: Git never looks inside that folder. Writing `logs/*` instead of
> `logs/` and adding `!logs/keep.txt` works.

## Why is it ignored? `git check-ignore -v`

If you can't figure out why a file doesn't show up, ask Git:

```text
~/app (main) $ git check-ignore -v debug.log
.gitignore:1:*.log      debug.log
~/app (main) $ git check-ignore -v build/app.exe
.gitignore:2:build/     build/app.exe
~/app (main) $ git check-ignore -v app.py
```

The output: which file (`.gitignore`), which line and which pattern. For a
file that is not ignored it prints nothing.

## Adding it anyway: `git add -f`

If you try to add an ignored file by name, Git warns you. If you really want
it, use `-f` (*force*):

```text
~/app (main) $ git add debug.log
The following paths are ignored by one of your .gitignore files:
debug.log
hint: Use -f if you really want to add them.
hint: Disable this message with "git config set advice.addIgnoredFile false"
~/app (main) $ git add -f debug.log
~/app (main) $ git status -s
A  debug.log
?? .gitignore
?? app.py
```

## An already tracked file

`.gitignore` only affects **untracked** files. Once a file has been
committed, writing it into `.gitignore` is not enough; Git keeps showing its
changes. You have to stop tracking it first: `git rm --cached` (the file
stays in the folder).

```text
~/app (main) $ echo "settings.local.json" > .gitignore
~/app (main) $ git status -s
 M settings.local.json
?? .gitignore
~/app (main) $ git rm --cached settings.local.json
rm 'settings.local.json'
~/app (main) $ git add .gitignore
~/app (main) $ git status -s
A  .gitignore
D  settings.local.json
~/app (main) $ git commit -m "Stop tracking local settings"
[main c67c262] Stop tracking local settings
 2 files changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 .gitignore
 delete mode 100644 settings.local.json
~/app (main) $ git status -s
~/app (main) $ ls
app.py  settings.local.json
```

From now on `settings.local.json` stays in the folder but Git doesn't see it.

> ⚠ **Once a secret has been committed** (a password, an API key), writing
> the file into `.gitignore` does **not remove it from the history**: it is
> still in the old commits. If the repository went to GitHub, **change** that
> password right away; consider it exposed. Best is to put files like `.env`
> into `.gitignore` before the first commit.

## Ready-made templates

There are ready-made `.gitignore` templates for every language and tool:
GitHub's `github/gitignore` repository and the "Add .gitignore" option when
you create a new repository on GitHub. A typical start for a Python / data
science project:

```text
# Python
__pycache__/
*.pyc
.venv/

# Secret settings
.env

# Jupyter
.ipynb_checkpoints/

# Big data and outputs
data/raw/
*.parquet
models/

# Editor and operating system
.vscode/
.DS_Store
Thumbs.db
```

## Only on your computer

`.gitignore` is shared with everyone. For patterns that only concern you
there are two more places:

- `.git/info/exclude`: same format, but only for this repository and only
  for you (not committed).
- A global file: `git config --global core.excludesFile ~/.gitignore_global`
  for all your repositories (e.g. the operating system's `Thumbs.db`).

## Summary

- `.gitignore` sits at the repository root; each line is a pattern. It is
  committed itself.
- `*` anything, trailing `/` folders only, leading `/` root only, `**/` any
  depth, `!` exception; the last matching rule wins.
- `git status --ignored` shows the ignored files, `git check-ignore -v file`
  the reason.
- `git add -f` adds an ignored file anyway.
- For an already tracked file, first `git rm --cached`.
- A committed password is not saved by `.gitignore`: change it.
