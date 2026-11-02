The user system behind permissions, and working as an administrator on a real
Linux system. This terminal has no `sudo` and no switching of users; what is
written here will help you on a real system.

## Users and groups

- Every file has an **owner** and a **group** (the two names in `ls -l`).
- Every user has a number (*uid*); `id` shows it.
- A user can be in several groups. A team is gathered in a group, the shared
  files are given that group, and `g+w` is added.
- The list of users is in `/etc/passwd`; the passwords are not there but in a
  separate file only root can read.

## root

**root** (uid 0) is the system's administrator; permissions do not stop it.
That is why daily work is not done as root: one typo could delete the whole
system.

## sudo

You write `sudo` in front of **a single** command that needs administrator
rights:

```bash
sudo apt install tree        # installing a program
sudo nano /etc/hosts         # editing a system file
```

sudo asks for your own password (not root's) and runs the command as root.
Only users who have been given the right can use it.

Rules:

- Do not add `sudo` just because a command said `Permission denied`. First
  ask: do I really need to change this file, am I in the wrong folder?
- Do not run commands with `sudo` copied from the internet without
  understanding them.
- Files in your own home folder do not need sudo. If they seem to, the file was
  created as root at some point.

## Changing the owner

`chown user:group file` changes a file's owner and group; it is usually used
with `sudo`. Not available in this terminal.

## Permissions in Git Bash

The Windows file system does not keep Linux permissions. In Git Bash `chmod`
is mostly without effect, and `ls -l` shows your Windows user as the owner.
Permissions matter on Linux, on a server or in a Docker container; the terminal
in this course imitates them so that they behave as on Linux.
