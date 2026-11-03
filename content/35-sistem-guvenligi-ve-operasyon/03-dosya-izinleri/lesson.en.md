# File Permissions

In the Operating System Security section we saw that the kernel checks
every request. The most frequently asked question is this: **may this user
read, change or run this file?** File permissions give the answer. A wrong
permission can make even the strongest encryption useless: a key file that
everyone can read means the key is not secret at all.

This section covers the **Unix permission model** used on Linux and macOS;
we touch on Windows' different model briefly at the end. The code is again
a toy: it does not touch real files, it calculates permissions with numbers
and dicts.

## Three classes, three permissions

Every file has an **owner** and a **group**. Anyone who wants to reach the
file falls into one of three classes:

- **Owner** (user, `u`): the user who owns the file.
- **Group** (`g`): the users in the file's group.
- **Others** (other, `o`): everyone else.

Each class has three permissions: **read** (`r`), **write** (`w`) and
**execute** (`x`). On folders, `x` means being able to enter the folder.
The nine permissions in total are written as a nine-letter string such as
`rwxr-xr--`: the first three letters are the owner's, the next three the
group's, the last three the others'.

## Writing it as a number: octal permissions

Each letter is a bit: `r` = 4, `w` = 2, `x` = 1. A class's permission is
their sum: `rwx` = 7, `r-x` = 5, `r--` = 4. Writing the digits of the three
classes side by side gives the **octal** permission: `755`, `644`, `600`.
In Python an octal number is written with `0o`, and `stat.filemode` from
the standard library turns a number into a string like the one in
`ls -l`:

```python
import stat

for mode in [0o755, 0o644, 0o600, 0o777]:
    print(oct(mode), stat.filemode(stat.S_IFREG | mode))
```

```text
0o755 -rwxr-xr-x
0o644 -rw-r--r--
0o600 -rw-------
0o777 -rwxrwxrwx
```

The leading `-` shows it is an ordinary file (`d` for a folder). We can
do the same conversion ourselves: we shift and read the three bits of each
class in turn.

```python
def to_string(mode):
    letters = ""
    for shift in (6, 3, 0):
        bits = (mode >> shift) & 7
        letters += "r" if bits & 4 else "-"
        letters += "w" if bits & 2 else "-"
        letters += "x" if bits & 1 else "-"
    return letters


print(to_string(0o750))
print(0o750, 7 * 64 + 5 * 8 + 0)
```

```text
rwxr-x---
488 488
```

`750` gives the owner everything, the group read and execute, and the
others nothing. The decimal value of the octal number is 488:
each digit is multiplied by a power of 8 (`7 × 64 + 5 × 8 + 0`).

| Permission | String | For what? |
|---|---|---|
| `755` | `rwxr-xr-x` | Programs, folders anyone may enter |
| `644` | `rw-r--r--` | Ordinary files anyone may read |
| `600` | `rw-------` | Secret files: keys, password files |
| `700` | `rwx------` | Folders only the owner may enter |
| `777` | `rwxrwxrwx` | Everyone does everything: almost always wrong |

## Which class? Only one

The most misunderstood rule of Unix permissions: the system chooses **a
single class** for the person accessing and looks only at that class's
bits. If they are the owner, the owner bits; if not and they are in the
group, the group bits; if neither, the others. The classes are **not
added up**.

<figure class="fig"><div class="flow">
  <span class="node">Request</span><span class="arrow">→</span>
  <span class="node acc">Owner?</span><span class="arrow">→</span>
  <span class="node acc">In the group?</span><span class="arrow">→</span>
  <span class="node">Others</span><span class="arrow">→</span>
  <span class="node ok">That class's bits</span>
</div><figcaption>The first matching class is chosen; the other classes' bits are never looked at.</figcaption></figure>

```python
def can(file, user, groups, action):
    bit = {"r": 4, "w": 2, "x": 1}[action]
    if user == file["owner"]:
        bits = (file["mode"] >> 6) & 7
    elif file["group"] in groups:
        bits = (file["mode"] >> 3) & 7
    else:
        bits = file["mode"] & 7
    return bool(bits & bit)


report = {"owner": "ada", "group": "staff", "mode": 0o640}
print(can(report, "ada", ["staff"], "w"))
print(can(report, "bob", ["staff"], "r"))
print(can(report, "bob", ["staff"], "w"))
print(can(report, "eve", ["guests"], "r"))
```

```text
True
True
False
False
```

The owner `ada` can write the report with permission `640`; `bob`, in the
group, can only read; `eve`, outside the group, can do nothing. The rule
works the other way round too: a file with permission `077` **cannot be
read by its owner**, while the group and the others can. Ownership is not
a privilege, it only decides which three bits are looked at.

## A new file's permission: umask

When a program creates a new file, where does its permission come from?
A program usually asks for `666` for files and `777` for folders; the
operating system removes the bits in a mask called the **umask**:

```python
for umask in [0o022, 0o077]:
    file_mode = 0o666 & ~umask
    dir_mode = 0o777 & ~umask
    print(oct(umask), oct(file_mode), oct(dir_mode))
```

```text
0o22 0o644 0o755
0o77 0o600 0o700
```

The common umask `022` removes write permission from the group and the
others: files become `644`, folders `755`. Where only the owner should have
access (a user's home folder, a service's secret data) `077` is used: files
become `600`, folders `700`. A umask only **removes** permissions, it never
adds any.

## Checking permissions

Permission mistakes gather in two places: files **anyone can write** and
files that **should be secret but others can read**. Both are found by
looking at the bits of the permission number:

```python
FILES = [
    {"path": "/srv/app/config.ini", "mode": 0o666},
    {"path": "/srv/app/run.sh", "mode": 0o755},
    {"path": "/home/ada/.ssh/id_key", "mode": 0o644},
]
for f in FILES:
    if f["mode"] & 0o002:
        print(f["path"], "world-writable")
    if f["path"].endswith("_key") and f["mode"] & 0o077:
        print(f["path"], "key readable by others")
```

```text
/srv/app/config.ini world-writable
/home/ada/.ssh/id_key key readable by others
```

Anyone can change the configuration file: someone could break the
program's settings or point it somewhere else. Anyone can read the key
file: the key is no longer secret. The program file, with `755`, is as it
should be. That is why many programs **refuse** to use a key file whose
permission is too wide; that is the right behaviour.

## Special bits and Windows

- **setuid / setgid:** the program runs with the privilege of the **file's
  owner** (or group), not of the person running it. It is needed for jobs
  such as changing a password, but every setuid program owned by an
  administrator is a potential door to privilege escalation, the topic of
  the next section; their number is kept small and checked regularly.
- **Sticky bit:** in a folder anyone can write to (such as `/tmp`), it lets
  each person delete only **their own** files.
- **Windows** uses **access control lists** (ACLs) instead of nine bits:
  for every file, a list of lines saying "this user or group, these
  permissions". The model is more detailed but the principle is the same:
  least privilege, open a secret file only to its owner.

## Summary

- Three classes (**owner**, **group**, **others**), three permissions
  (**r**, **w**, **x**); `r` = 4, `w` = 2, `x` = 1.
- Octal permissions: `755` for programs, `644` for ordinary files, `600`
  for secret files; `777` is almost always wrong.
- **A single class** is chosen for the person accessing; the classes are
  not added up.
- The **umask** **removes** bits from a new file's permission: `022` →
  `644` / `755`, `077` → `600` / `700`.
- Two things to check: files anyone can write and secret files others can
  read.
