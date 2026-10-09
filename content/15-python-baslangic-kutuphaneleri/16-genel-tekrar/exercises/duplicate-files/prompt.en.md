There is a `files` folder with subfolders next to your file; some files
have the same content. Write the function `duplicate_files(folder)`: group
all files (`rglob`) by their content (`defaultdict(list)`, the key is
`read_text`) and take the groups with **more than one** file. Each group is a
**sorted** list of paths relative to `folder` with `/` separators; return the
list of groups sorted too.

**Expected output:**

```
['a.txt', 'copy/a2.txt', 'notes.txt']
['b.txt', 'c.txt']
```
