# Installing and First Settings

The practice terminal imitates Git, but for your real projects Git has to
be installed on your own computer. In this section we will install Git and
make the settings you do **once**: your name, your e-mail, the branch name
for new repositories and your editor. Without them you cannot even make the
first commit.

## Is it installed?

Let's check first; it may already be there. Open a terminal (**Git Bash** or
**PowerShell** from the Start menu on Windows, **Terminal** on Mac) and type:

```bash
git --version
```

If you see a line like `git version 2.55.0`, Git is installed and you can
skip the installation part. If you get an error like "command not found" or
"is not recognized", you need to install it.

## Installing on Windows

1. Go to **git-scm.com** and click **Download for Windows**. The file you
   get is an installer named like `Git-2.xx.x-64-bit.exe`.
2. Run the installer. Many screens follow; on most of them keeping the
   default and clicking **Next** is enough. Four screens are worth a look:

| Screen | Choice | Why |
|---|---|---|
| *Choosing the default editor* | **Visual Studio Code** (if installed) or **Notepad** | The default is Vim; someone who doesn't know how to quit it can get stuck there. |
| *Adjusting the name of the initial branch* | **Override…**, name **main** | New repositories get `main` as their main branch, like on GitHub. |
| *Adjusting your PATH* | **Git from the command line and also from 3rd-party software** | Git also works from PowerShell and VS Code. |
| *Configuring the line ending conversions* | **Checkout Windows-style, commit Unix-style** | Line endings are stored one way in the repository (see below). |

3. When it finishes, **Git Bash** appears in the Start menu. Open it and
   type `git --version`.

If you like the command line, Windows' package manager can install it too:

```bash
winget install --id Git.Git -e --source winget
```

## Installing on Mac and Linux

**Mac:** typing `git --version` in Terminal is enough. If Git is missing,
macOS offers to install the "command line developer tools"; click
**Install**. If you use Homebrew, `brew install git` installs the newest
version.

**Linux:** use your distribution's package manager:

```bash
sudo apt install git     # Ubuntu, Debian
sudo dnf install git     # Fedora
```

## Who are you? `user.name` and `user.email`

Every commit carries its author's name and e-mail (you saw this in the last
section). Git reads them from your settings; without them it refuses to
commit. On an unconfigured computer the first commit shows this:

```text
~/notes (main) $ git commit -m "Add todo list"
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'ada@odyssey.(none)')
```

Git even tells you what to do. Let's set them:

```text
~ $ git config --global user.name "Ada Lovelace"
~ $ git config --global user.email ada@example.com
~ $ git config user.name
Ada Lovelace
~ $ git config user.email
ada@example.com
```

- `git config` reads and writes settings. `--global` means "for all my
  repositories on this computer".
- We wrote the name **in quotes** because it contains a space. Without the
  quotes Git takes only the `Ada` part.
- To read a value, leave out the value: `git config user.name`. If it is set
  it prints the value, otherwise it prints nothing.

> **Which e-mail?** If you will use GitHub, make it the same as the e-mail
> on your GitHub account; that is how GitHub matches commits to you. If you
> don't want your e-mail to appear in public commits, you can use the
> `…@users.noreply.github.com` address GitHub gives you (GitHub › Settings ›
> Emails).

## The branch name for new repositories

When Git creates a repository it gives the main branch a name. Older versions
said `master`; today most projects and GitHub use `main`. If you didn't pick
it during installation, set it once:

```bash
git config --global init.defaultBranch main
```

From then on every `git init` starts with a `main` branch.

## The editor: `core.editor`

Some commands (such as `git commit` without a message) open an editor for
you to type in. If you didn't choose one during installation, Vim opens; to
quit Vim you press `Esc`, then `:q` and `Enter`. That is an unpleasant
surprise for someone who doesn't know it. If you use VS Code:

```bash
git config --global core.editor "code --wait"
```

`--wait` matters: Git waits until you close the file. Without it, Git carries
on with an empty message as soon as VS Code opens.

> No editor opens in Odyssey's practice terminal; we will always write commit
> messages with `-m` (next section).

## Where do settings live? Three levels

Git keeps settings in three places. If the same setting is in more than one,
the **narrowest** one wins:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>System (--system)</span><span>A file where Git is installed. For everyone on the computer. The installer writes it; you rarely touch it.</span></div>
    <div class="anat-row"><span>Global (--global)</span><span>~/.gitconfig. For all your repositories. Your name, e-mail and editor go here.</span></div>
    <div class="anat-row"><span>Repository (--local)</span><span>.git/config. For that repository only. Without an option, git config writes here.</span></div>
  </div>
  <figcaption>Lower overrides higher: the repository setting beats the global one, the global one beats the system one.</figcaption>
</figure>

Usually `--global` is all you need. The repository level is for cases that
need a different identity: for example, using your work e-mail in work
projects.

```text
~/work (main) $ git config user.email ada@company.example
~/work (main) $ git config --list --show-origin
file:/home/ada/.gitconfig       user.name=Ada Lovelace
file:/home/ada/.gitconfig       user.email=ada@example.com
file:/home/ada/.gitconfig       init.defaultbranch=main
file:.git/config        core.repositoryformatversion=0
file:.git/config        core.filemode=false
file:.git/config        core.bare=false
file:.git/config        core.logallrefupdates=true
file:.git/config        core.symlinks=false
file:.git/config        core.ignorecase=true
file:.git/config        user.email=ada@company.example
~/work (main) $ git config user.email
ada@company.example
```

`--show-origin` shows which file each setting comes from. Here `user.email`
is in two places; in this repository the one in `.git/config` wins, in any
other repository the global one applies.

## Seeing and fixing settings

| Command | What it does |
|---|---|
| `git config --list` | All settings in effect (global first, then repository). |
| `git config --global --list` | Only global settings (`~/.gitconfig`). |
| `git config --list --show-origin` | With the file each setting comes from. |
| `git config user.name` | The value of one setting. |
| `git config --global user.name "New Name"` | Change a setting (overwrites the old one). |
| `git config --global --unset core.editor` | Remove a setting. |

The settings files are plain text; you can open and read them:

```text
[user]
	name = Ada Lovelace
	email = ada@example.com
[init]
	defaultBranch = main
[core]
	editor = code --wait
```

## Line endings on Windows

Windows ends a line in a text file with two characters (`CRLF`), Mac and
Linux with one (`LF`). In a mixed team this difference can make every line
look "changed". The *Checkout Windows-style, commit Unix-style* option we
chose during installation sets `core.autocrlf=true`: `LF` goes into the
repository, `CRLF` comes into your folder. You don't need to do anything; if
you see the warning "LF will be replaced by CRLF", this is why, and it is
harmless.

## Summary

- `git --version` tells you whether Git is installed.
- On Windows, install from git-scm.com; watch the editor, `main` branch name,
  PATH and line ending screens.
- Once, before committing: `user.name` and `user.email`.
- `init.defaultBranch main` sets the branch name of new repositories.
- `core.editor "code --wait"` makes Git use VS Code.
- Settings live on three levels: system, global (`--global`), repository. The
  narrowest wins.
