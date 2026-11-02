All the forms of variables, at a glance.

## Defining and using

| Form | What it does |
|---|---|
| `name=Ada` | Defines it; no spaces around `=` |
| `name="Ada Lovelace"` | A value with spaces goes in quotes |
| `echo "$name"` | Uses the value |
| `echo "${name}_2026"` | The end of the name is clear |
| `echo '$name'` | Not expanded in single quotes: prints `$name` |
| `unset name` | Removes it |

## Expansions

| Form | Result |
|---|---|
| `$(command)` | The command's output |
| `$((3 * 4))` | `12` (integers) |
| `${name:-backup}` | `backup` if `name` is empty |
| `${#name}` | The length of the value |

## The environment

| Form | What it does |
|---|---|
| `export NAME=value` | An environment variable (child programs see it) |
| `export name` | Moves an existing variable into the environment |
| `NAME=value command` | Only for that command |
| `env` | Every environment variable |
| `printenv NAME` | A single environment variable |

## Ready-made variables

| Name | Value |
|---|---|
| `HOME` | The home folder |
| `USER` | The user name |
| `PWD` | The current folder |
| `SHELL` | The shell in use |
| `PATH` | The folders where commands are looked for (with `:`) |

## Remember

- Give your own variables lower-case names; the capitalised ones belong to
  the system.
- Always use a variable that may contain spaces as `"$name"`.
- An undefined variable gives no error, it is empty: make sure you spelled the
  name right.
