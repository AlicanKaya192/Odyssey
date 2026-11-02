Every part of a script, at a glance.

## Skeleton

```bash
#!/bin/bash
# One line saying what it does.

if [ -z "$1" ]; then
  echo "usage: script.sh FILE"
  exit 1
fi

for f in "$@"; do
  echo "processing $f"
done
```

## Running

| Form | What it needs |
|---|---|
| `bash script.sh` | Read permission |
| `./script.sh` | `chmod +x`, a shebang |
| `script.sh` | Its folder must be in PATH |
| `source script.sh` | Runs in the current shell; its variables stay |

## Special variables

| Name | Value |
|---|---|
| `$0` | The script's name |
| `$1` ... `$9` | The arguments |
| `$#` | The number of arguments |
| `"$@"` | All the arguments, one by one |
| `$?` | The exit code of the last command |

## Tests

| Test | Meaning |
|---|---|
| `[ -f path ]` | A file exists |
| `[ -d path ]` | A folder exists |
| `[ -z "$a" ]` | Empty |
| `[ "$a" = "b" ]` | Texts are equal |
| `[ $n -gt 0 ]` | Number is greater (`-eq -ne -lt -le -ge`) |

## Loops and a function

```bash
for i in $(seq 1 3); do echo "$i"; done
while [ $n -gt 0 ]; do n=$((n - 1)); done
greet() { local name=$1; echo "Hi, $name"; }
```
