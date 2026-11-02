The most common mistakes with redirection and why they happen.

## 1. Writing over the file you are reading

```bash
sort names.txt > names.txt
```

The shell first opens `names.txt` for writing and **empties** it, then runs
`sort`. `sort` reads an empty file; the result is an empty file. The right
way:

```bash
sort names.txt > sorted.txt
```

## 2. Forgetting `>>` instead of `>`

If you write to a log file with `>` every time, only the last line stays. For
every file you want to build up, use `>>`.

## 3. The error message did not go into the file

`command > out.txt` only redirects stdout. Error messages stay on the screen.
If you want the errors too, use `> out.txt 2>&1`.

## 4. `2>&1` in the wrong place

| Spelling | Result |
|---|---|
| `command > f 2>&1` | Both into f |
| `command 2>&1 > f` | Errors **to the screen**, output into f |

The shell applies redirections from left to right. In the second line, at the
moment `2>&1` was written, stdout was still going to the screen.

## 5. A file you never made appeared

`command > result.txt` opens `result.txt` even if the command fails. If you
see an empty file, first check whether the command gave an error.

## 6. `2>1`

If you forget the `&`, `1` is taken as a file name and the errors are written
into a file called `1`. The right way is `2>&1`.
