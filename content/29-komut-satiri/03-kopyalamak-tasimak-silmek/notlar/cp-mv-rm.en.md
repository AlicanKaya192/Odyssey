The commands of this section, at a glance.

## cp

| Command | What it does |
|---|---|
| `cp a.txt b.txt` | A copy of a.txt named b.txt (overwrites if it exists) |
| `cp a.txt backup/` | Copies it as `backup/a.txt` |
| `cp a.txt b.txt backup/` | Both into the folder |
| `cp -r site site-backup` | Copies a folder with its contents |

## mv

| Command | What it does |
|---|---|
| `mv old.txt new.txt` | Renames |
| `mv a.txt archive/` | Moves into the folder |
| `mv a.txt b.txt archive/` | Moves both |
| `mv draft final` | Renames a folder (no option needed) |

## rm

| Command | What it does |
|---|---|
| `rm a.txt` | Deletes the file |
| `rm a.txt b.txt` | Several files |
| `rm -r tmp` | Deletes a folder with its contents |
| `rm -f a.txt` | Never asks, no complaint if it is missing |
| `rm -i a.txt` | Asks for each file (in a real terminal) |
| `rmdir empty` | Only an empty folder |

## Errors

| What you see | Meaning |
|---|---|
| `cp: cannot stat 'x': No such file or directory` | The source does not exist |
| `cp: -r not specified; omitting directory 'd'` | `-r` forgotten for a folder |
| `cp: target 'x' is not a directory` | Several sources, the target is not a folder |
| `rm: cannot remove 'd': Is a directory` | Use `rm -r` for a folder |
| `mv: cannot move 'a' to 'x/a': No such file or directory` | The target folder does not exist |
