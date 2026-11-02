An `ls -l` line, from left to right.

```text
drwxr-xr-x 2 ada ada 4096 Oct  7 10:00 src/
-rw-r--r-- 1 ada ada  292 Oct  7 10:00 report.txt
```

| Column | Example | Meaning |
|---|---|---|
| 1st character | `d` / `-` | Folder / regular file |
| Characters 2–10 | `rwxr-xr-x` | Permissions: owner, group, others (three letters each) |
| Number | `2` / `1` | Link count (grows with subfolders in a folder) |
| Name | `ada` | Owner |
| Name | `ada` | Group |
| Number | `4096` / `292` | Size (bytes); `4.0K` with `-h` |
| Date | `Oct  7 10:00` | Last change; old files show the year instead of the time |
| Name | `src/` | The name; this terminal and Git Bash add `/` to folders |

## Frequently asked

- **Why is a folder 4096?** The disk block of the folder's entry. For the
  total of its contents another command is used (`du -sh folder`).
- **A file with size 0?** An empty file, often created with `touch`.
- **Why `ada` twice?** One is the user, one is the group. On Linux every user
  has a group with their own name.
- **What is `total`?** The total blocks on disk; not the number of files.
- **A `*` at the end of the line?** An executable file (Permissions section).
