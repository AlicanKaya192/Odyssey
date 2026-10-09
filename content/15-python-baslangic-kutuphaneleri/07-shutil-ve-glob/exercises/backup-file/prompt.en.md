There is a `notes.txt` next to your file. Write the function
`backup_file(path, folder)`: create the `folder` folder (with the ones in
between), copy the file into it keeping its time (`shutil.copy2`) and return
the new file's path as text with `/` separators (`Path(...).as_posix()`).

**Expected output:**

```
backup/notes.txt
Meeting at 10.
```
