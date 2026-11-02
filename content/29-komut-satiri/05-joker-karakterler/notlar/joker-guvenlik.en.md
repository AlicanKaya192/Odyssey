Wildcards are powerful; combined with `rm`, `mv` and `cp`, one wrong
character affects many files. These four habits prevent most accidents.

## 1. echo first

Put `echo` in front of the real command and run it:

```bash
echo rm *.tmp
```

You see the exact command that would run. If it is right, remove `echo` and
run it again (up arrow, start of the line, delete).

## 2. Watch the spaces

| What you type | What it means |
|---|---|
| `rm *.tmp` | Files ending in `.tmp` |
| `rm * .tmp` | **Everything**, and a file named `.tmp` |
| `rm *tmp` | Everything ending in `tmp` (`.tmp` and `notes-tmp` too) |

## 3. Where are you?

`*` is expanded relative to the folder you are in. Before typing
`rm *.log`, run `pwd`. Writing the path into the pattern is safer:
`rm ~/project/logs/*.log`.

## 4. Quote the pattern when a program should get it

Commands like `find` interpret the pattern themselves. Without quotes the
shell expands it first and something else goes to the program:

```bash
find . -name "*.txt"
```

The rule from this section applies here too: wildcards are not expanded
inside quotes.
