## Bits

| Letter | Permission | Value | On a folder |
|---|---|---|---|
| `r` | Read | 4 | Listing its contents |
| `w` | Write | 2 | Creating and deleting files in it |
| `x` | Execute | 1 | Entering it |

Classes: owner (`u`), group (`g`), others (`o`). In an octal permission
the first digit is the owner's, the second the group's, the third the
others'.

## Common permissions

| Octal | Decimal | String | Use |
|---|---|---|---|
| `755` | 493 | `rwxr-xr-x` | A program, a shared folder |
| `750` | 488 | `rwxr-x---` | A program for the group |
| `644` | 420 | `rw-r--r--` | An ordinary file |
| `640` | 416 | `rw-r-----` | A file the group reads |
| `600` | 384 | `rw-------` | A key, a password file |
| `700` | 448 | `rwx------` | A private folder |

## On the command line

| Command | What does it do? |
|---|---|
| `ls -l file` | Shows the permission string, the owner and the group |
| `chmod 600 file` | Sets the permission in octal |
| `chmod o-w file` | Removes write permission from the others |
| `chown ada:staff file` | Changes the owner and the group |
| `umask` | Shows the current mask |

## Python patterns

- A class's bits: owner `(mode >> 6) & 7`, group `(mode >> 3) & 7`,
  others `mode & 7`.
- Can anyone write: `mode & 0o002`.
- Can anyone but the owner do anything: `mode & 0o077`.
- Applying a umask: `base & ~umask`.
- Octal text: `oct(0o644)` → `'0o644'`; back again with `int("644", 8)`.

## Keep in mind

- A single class is chosen: the owner looks at the owner bits; the owner
  cannot read a file with permission `077`.
- A umask only removes.
- `777` and a key file anyone can read are the first two mistakes looked
  for in a check.
