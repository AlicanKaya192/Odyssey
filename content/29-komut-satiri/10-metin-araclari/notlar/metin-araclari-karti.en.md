The options of the four tools, at a glance.

## sort

| Form | What it does |
|---|---|
| `sort f` | Alphabetical order (as text) |
| `sort -r f` | Reversed order |
| `sort -n f` | By numeric value |
| `sort -u f` | Sorts and drops repeats |
| `sort -t , -k 3 f` | From the 3rd comma-separated field on |
| `sort -t , -k 3,3 f` | Only by the 3rd field |
| `sort -t , -k 3 -rn f` | By the 3rd field, biggest first |

## uniq

| Form | What it does |
|---|---|
| `uniq` | Reduces identical neighbouring lines to one |
| `uniq -c` | Writes the repeat count in front |
| `uniq -d` | Only the repeated ones (once each) |
| `uniq -u` | Only the ones that appear once |
| `uniq -i` | Ignoring upper/lower case |

Almost always there is a `sort` in front of it.

## cut

| Form | What it does |
|---|---|
| `cut -d , -f 2` | The 2nd field |
| `cut -d , -f 1,3` | Fields 1 and 3 |
| `cut -d , -f 2-4` | From 2 to 4 |
| `cut -d ' ' -f 3-` | From the 3rd field to the end |
| `cut -c 1-10` | The first 10 characters |

Without a delimiter, a tab (`Tab`) is assumed.

## tr

| Form | What it does |
|---|---|
| `tr a-z A-Z` | Lower case to upper case |
| `tr '[:upper:]' '[:lower:]'` | Upper case to lower case |
| `tr -d '0-9'` | Deletes the digits |
| `tr -s ' '` | Squeezes repeated spaces into one |
| `tr , '\n'` | Turns commas into line breaks |

`tr` takes no file name: `tr ... < f` or <code>cat f &#124; tr ...</code>.
