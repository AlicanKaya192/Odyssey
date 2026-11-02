All the permissions, at a glance.

## Reading them

```text
-rwxr-xr--
│└┬┘└┬┘└┬┘
│ │  │  └ others (o)
│ │  └─── group (g)
│ └────── owner (u)
└──────── type: - file, d folder
```

## Letters

| Permission | On a file | On a folder |
|---|---|---|
| `r` | Read what is inside | List what is inside |
| `w` | Change what is inside | Create, delete, rename files in it |
| `x` | Run it as a program | Enter it, reach what is inside |

## Numbers

| Digit | Permission | Digit | Permission |
|---|---|---|---|
| 7 | `rwx` | 3 | `-wx` |
| 6 | `rw-` | 2 | `-w-` |
| 5 | `r-x` | 1 | `--x` |
| 4 | `r--` | 0 | `---` |

| Number | Looks like | When |
|---|---|---|
| 644 | `rw-r--r--` | A regular file |
| 600 | `rw-------` | A secret file (a key, a password file) |
| 755 | `rwxr-xr-x` | A script, a program, a folder |
| 700 | `rwx------` | A folder that is yours only |
| 444 | `r--r--r--` | Read only |

## chmod

| Form | What it does |
|---|---|
| `chmod +x f` | Adds execute for everyone |
| `chmod u+x f` | Adds execute only for the owner |
| `chmod go-rwx f` | Removes every permission from the group and others |
| `chmod a=r f` | Exactly read only, for everyone |
| `chmod g+w,o-r f` | Two changes at once |
| `chmod 600 f` | With a number, writes all of them from scratch |

## Remember

- `./script` needs `x`; `bash script` only needs `r`.
- Every folder on the way to a file needs `x`.
- `chmod 777` is easy but unsafe; give the least permission.
