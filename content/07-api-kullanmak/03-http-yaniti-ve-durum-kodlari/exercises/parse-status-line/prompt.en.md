The status line has three parts: the version, the code and the reason phrase.
But careful: the phrase itself may contain spaces (`Not Found`, `Too Many
Requests`). A plain `split(" ")` breaks the phrase into pieces.

**What to do:**

1. Write the function `parse_status_line(line)`: it returns
   `{"version": ..., "code": ..., "reason": ...}`. `code` must be a
   **number** (int). Split at most twice: `line.split(" ", 2)`.
2. For every line in the `lines` list, print the code and the reason as
   below; at the end print how many were successful.

**Expected output:**

```
200 | OK
404 | Not Found
429 | Too Many Requests
201 | Created
successful: 2
```
