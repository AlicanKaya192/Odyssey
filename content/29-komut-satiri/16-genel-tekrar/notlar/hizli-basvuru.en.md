Every command of the path, on one page.

## Moving around

| Command | What it does |
|---|---|
| `pwd` | The current folder |
| `ls`, `ls -la`, `ls -lh` | List; details, hidden ones, readable sizes |
| `cd path`, `cd ..`, `cd ~`, `cd -` | Go; up, home, previous |
| `clear` (Ctrl+L) | Clear the screen |

## Files and folders

| Command | What it does |
|---|---|
| `mkdir -p a/b` | A folder (with its parents) |
| `touch f` | An empty file |
| `cp f g`, `cp -r d e` | Copy; with a folder |
| `mv f g` | Move or rename |
| `rm f`, `rm -r d`, `rmdir d` | Delete (cannot be undone) |

## Looking inside

| Command | What it does |
|---|---|
| `cat f`, `cat -n f` | All of it; numbered |
| `head -n 5 f`, `tail -n 5 f` | Start, end |
| `tail -n +2 f` | From line 2 to the end |
| `wc -l f` | The number of lines |

## Wildcards

`*` any text, `?` one character, `[abc]` one of them, `{a,b}` both.
The shell expands them; not inside quotes.

## Redirection and pipes

| Form | What it does |
|---|---|
| `c > f`, `c >> f` | Output into a file; add to the end |
| `c 2> f`, `c > f 2>&1` | Errors; both at once |
| `c 2> /dev/null` | Drop the errors |
| `c < f` | Input from a file |
| <code>a &#124; b</code> | a's output is b's input |

## Text

| Command | What it does |
|---|---|
| `grep -i -n -c -v -w -o 'pattern' f` | Search lines |
| <code>grep -E 'A&#124;B'</code>, `grep -rl 'w' .` | Or; file names |
| `sort -r -n -u`, `sort -t , -k 3` | Sort |
| `uniq -c -d -u` | Neighbouring repeats |
| `cut -d , -f 2`, `cut -c 1-10` | Field, characters |
| `tr a-z A-Z`, `tr -d x`, `tr -s ' '` | Translate, delete, squeeze |

## Finding

`find path -name '*.py' -type f -maxdepth 2`, `-iname`, `-not`,
`-exec c {} \;`, `-delete` (list first).

## Permissions

`ls -l` → `-rwxr-xr--` (owner, group, others). `chmod +x f`, `chmod u-w f`,
`chmod 644 f` (r=4 w=2 x=1). On a folder `x` = entering it.

## Variables

| Form | What it does |
|---|---|
| `name=value`, `"$name"`, `"${name}"` | Define, use |
| `$(command)`, `$((a + 1))` | Output, arithmetic |
| `export NAME=value`, `env` | The environment |
| `export PATH="$HOME/bin:$PATH"` | Add to PATH |
| `source ~/.bashrc` | Read the settings again |

## Scripts and exit codes

| Form | What it does |
|---|---|
| `#!/bin/bash`, `chmod +x`, `./s.sh` | A script |
| `$1 $# "$@" $0` | Arguments |
| `if [ -f "$1" ]; then ...; fi` | A decision |
| `for x in ...; do ...; done` | A loop |
| `exit 1`, `echo $?` | Exit code |
| `a && b`, <code>a &#124;&#124; b</code>, `a ; b` | If it succeeded, if it failed, in every case |
