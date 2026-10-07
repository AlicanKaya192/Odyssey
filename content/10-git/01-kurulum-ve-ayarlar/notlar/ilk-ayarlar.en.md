What to do, in order, to get Git ready on a new computer. Each step is done
once.

## 1. Install

```bash
git --version
```

If a version line appears, it is installed. If not:

- **Windows:** git-scm.com → Download for Windows (or `winget install --id Git.Git -e --source winget`).
- **Mac:** accept the install offer that appears after `git --version`, or `brew install git`.
- **Linux:** `sudo apt install git` / `sudo dnf install git`.

## 2. Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

## 3. Defaults

```bash
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

## 4. Check

```bash
git config --global --list
```

Expected output (with your values):

```text
user.name=Ada Lovelace
user.email=ada@example.com
init.defaultbranch=main
core.editor=code --wait
```

Notice the key names are shown in lower case: you typed
`init.defaultBranch`, Git shows `init.defaultbranch`. Git does not care
about upper and lower case in setting names; both are the same setting.

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `Author identity unknown` | No name or e-mail. | Do step 2. |
| The commit's name is only `Ada` | You typed the name without quotes. | `git config --global user.name "Ada Lovelace"` |
| A setting works in one repository but not another | You forgot `--global`; the setting went into that repository's `.git/config`. | Run it again with `--global`; if needed, remove the repository one with `git config --unset user.name`. |
| A setting has no effect | Wrong key name: `user.mail`, `user.nmae`. Git saves the wrong name too, without a warning. | Look with `git config --list --show-origin`, remove the wrong one with `--unset`. |
| Commits are not linked to your GitHub profile | The e-mail differs from the one on GitHub. | Use the address in GitHub › Settings › Emails. |
| `git commit` without a message got stuck in Vim | The default editor is Vim. | Quit with `Esc`, `:q!`, `Enter`; set `core.editor`. |
