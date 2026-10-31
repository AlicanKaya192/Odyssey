Write a tool with `clap`: `<word>` is required, `--times` (`-t`) says how many times to write it, 1 by default. If `--upper` (`-u`) is given, it writes in capitals.

- `hi` → `hi`
- `hi -t 2` → two lines of `hi`
- `hi --upper` → `HI`
- No arguments: exit code 2
