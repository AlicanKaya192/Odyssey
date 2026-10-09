There are `part0.txt`, `part1.txt`, `part2.txt` next to your file. Write the
function `first_lines(paths)`: open all the files with `ExitStack`
(`enter_context`) and return the first line of each (`readline().strip()`) as
a list.

**Expected output:**

```
['line 0', 'line 1', 'line 2']
```
