Write the function `convert_args(argv)`: define one or more file names
(`nargs="+"`) and a `--format` that can be `csv` or `json` (default `csv`,
`choices`); return the list `[files, format]`.

**Expected output:**

```
[['a.txt', 'b.txt'], 'json']
[['x.txt'], 'csv']
```
