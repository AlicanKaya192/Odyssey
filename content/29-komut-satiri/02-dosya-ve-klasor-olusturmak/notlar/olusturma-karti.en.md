The commands of this section, at a glance.

| Command | What it does |
|---|---|
| `mkdir notes` | Creates the `notes` folder. |
| `mkdir a b c` | Three folders at once. |
| `mkdir -p site/css/img` | Together with missing parents; quiet if it exists. |
| `touch todo.txt` | An empty file; if it exists, only updates its time. |
| `touch a.txt b.txt` | Several empty files. |
| `echo "text" > f.txt` | Writes the file **from the start** (old content is gone). |
| `echo "text" >> f.txt` | Adds to the **end** of the file. |
| `cat f.txt` | Prints the contents of the file. |
| `cat a.txt b.txt` | Two files one after the other. |
| `cat -n f.txt` | With line numbers. |
| `rmdir empty` | Deletes a folder only if it is **empty**. |
| `touch .secret` | A hidden file (its name starts with a dot). |

## Writing a file of a few lines

```bash
echo "eggs" > shopping.txt
echo "bread" >> shopping.txt
echo "tea" >> shopping.txt
cat shopping.txt
```

The first line with `>`, the rest with `>>`. If you make a mistake, writing
the first line again with `>` resets the file.

## Common mistakes

| What you see | Why | What to do |
|---|---|---|
| `mkdir: cannot create directory 'a/b': No such file or directory` | `a` does not exist | `mkdir -p a/b` |
| `mkdir: cannot create directory 'a': File exists` | It already exists | Do nothing, or use `-p` |
| `rmdir: failed to remove 'x': Directory not empty` | The folder is not empty | Empty it (next section: `rm -r`) |
| `bash: notes/x.txt: No such file or directory` | `>` does not create folders | `mkdir notes` first |
| The old lines of the file disappeared | `>` instead of `>>` | Use `>>` from now on |
