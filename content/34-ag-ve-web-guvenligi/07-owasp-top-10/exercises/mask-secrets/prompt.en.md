`mask(line)` should replace the values of `password`, `token` and
`api_key` in a line to be logged with `***`, keeping the name
(`password=***`). A value runs up to `&` or a space. The starter code masks
only `password`.

**Expected output:**

```
user=ada&password=***
token=*** api_key=*** status=200
nothing secret here
```
