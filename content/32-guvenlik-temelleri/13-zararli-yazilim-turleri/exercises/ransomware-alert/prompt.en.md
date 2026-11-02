`stats` is a dictionary from program name to two numbers:
`files_written` and `extensions_changed`.

`ransomware_alert(stats, min_writes, min_ratio)` should return the names of
the suspicious programs in alphabetical order: the number of files written
is equal to or greater than `min_writes` **and** the extension-change ratio
(`extensions_changed / files_written`) is greater than `min_ratio`. A
program that wrote no files is not suspicious (do not divide by zero).

**Expected output:**

```
['unknown.exe']
['renamer.exe', 'unknown.exe']
```
