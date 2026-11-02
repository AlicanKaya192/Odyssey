`find ... -delete` and `find ... -exec rm {} \;` are powerful: they delete
hundreds of files in one line, and it **cannot be undone**. The terminal has no
recycle bin.

## Three steps

1. **List.** Run the command without deleting:
   `find project -name '*.bak'`
2. **Read.** Does the list hold only what you want to delete? Is the count what
   you expected? If needed, `| wc -l`.
3. Add `-delete` to **the same command**. Do not retype it; bring the previous
   command back with the arrow key and add it to the end. That way what you
   listed and what you delete are the same.

## Common mistakes

- **No quotes around the pattern.** `find . -name *.bak -delete` can turn into
  the name of a file in the current folder and delete something you did not
  expect (or nothing).
- **`-delete` written first.** find works through the conditions from left to
  right; if `-delete` comes before the conditions it deletes **everything**
  before any condition is applied. `-delete` always goes last.
- **-delete with no condition.** `find project -delete` deletes the whole
  project.
- **The wrong start path.** `find / ...` looks at the whole disk. Keep the start
  path as narrow as you can.

## Moving instead of deleting

If you are not sure, do not delete, move:

```bash
mkdir ../trash
find project -name '*.bak' -exec mv {} ../trash/ \;
```

If something turns out to be missing, you bring it back.
