There are two ways to connect to GitHub. The green **Code** button on a
repository's page gives the address for both.

| | HTTPS | SSH |
|---|---|---|
| Address | `https://github.com/ada/notes.git` | `git@github.com:ada/notes.git` |
| Identity | Browser sign-in or a personal access token | An SSH key on your computer |
| Setup | None on Windows (Git Credential Manager) | Create a key once and add it to GitHub |
| Obstacle | — | Some company networks block the SSH port |

**HTTPS** is enough to start: on the first `push` GitHub opens in the
browser, you approve, and Git Credential Manager remembers.

## An SSH key (optional)

```text
ssh-keygen -t ed25519 -C "ada@example.com"
```

You can press Enter through the questions (or set a passphrase for the key).
Two files are created: `~/.ssh/id_ed25519` (**secret**, never share it) and
`~/.ssh/id_ed25519.pub` (public). Paste the content of the public one into
GitHub › Settings › SSH and GPG keys › New SSH key. To test:

```text
ssh -T git@github.com
```

If you see `Hi ada! You've successfully authenticated`, you're done. To
switch an existing repository's address to SSH:

```text
git remote set-url origin git@github.com:ada/notes.git
```

## Personal access token

Where a browser can't open (servers, some tools), instead of a password you
create a token in GitHub › Settings › Developer settings › Personal access
tokens and paste it where the password is asked. A token is a password: it
is never written into a file, code or a commit.
