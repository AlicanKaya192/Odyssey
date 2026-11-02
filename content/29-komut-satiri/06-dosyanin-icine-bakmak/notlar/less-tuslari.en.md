`less` is used to read long files in a real Linux, macOS or Git Bash
terminal. It is not in Odyssey's terminal; here you have `head`, `tail` and
`cat -n`.

```text
$ less logs/server.log
```

## Keys

| Key | What it does |
|---|---|
| Space or `Page Down` | One page forward |
| `b` or `Page Up` | One page back |
| Down / up arrow | One line |
| `g` | To the start of the file |
| `G` | To the end of the file |
| `/word` and Enter | Search forward |
| `n` / `N` | Next / previous match |
| `q` | Quit |

## Good to know

- `less` does not change the file; you only read it.
- Manual pages like `man ls` also open in `less`; the same keys work there.
- `less +F file` follows the end like `tail -f`; `Ctrl+C` returns to the
  normal view.
- If you get stuck, press `q`. If you see `:` on the screen, `less` is still
  open.
