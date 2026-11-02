Exit codes and every way to make decisions with them.

## Common codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | A general error; "not found" for grep |
| 2 | Wrong use; "no such file" for ls and grep |
| 126 | Found but could not run (permission) |
| 127 | Command not found |
| 130 | Stopped with Ctrl+C |

## Reading and using them

| Form | What it does |
|---|---|
| `echo $?` | The last command's code |
| `code=$?` | Keeps the code (right after) |
| `exit 3` | Ends the script with code 3 |
| `true` / `false` | Always 0 / always 1 |

## Chains

| Form | When b runs |
|---|---|
| `a && b` | If a succeeded |
| <code>a &#124;&#124; b</code> | If a failed |
| `a ; b` | In every case |
| `! a && b` | If a failed |
| <code>a &amp;&amp; b &#124;&#124; c</code> | b if a succeeded; c if a or b failed |

## A command as a condition

```bash
if grep -q ERROR app.log; then
  echo "errors found"
fi
```

`if`, `while` and `&&` look at the command's **code**, not its output.

## Remember

- `$?` is rewritten after every command.
- A pipeline's code is that of its last command.
- `a && b || c` looks like an `if`/`else` but is not: if b fails, c runs too.
  For important decisions, write an `if`.
