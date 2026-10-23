Ask the user for their name and home and add a row to the end of `students.csv` with `csv.DictWriter` (columns `name`, `home`). The address may contain a comma (`Number Four, Privet Drive`); `csv` puts it in quotes. The file already has its header, do not write one. Open the file with `newline=""` so no blank lines appear on Windows.

Example run (the prompt can say anything you like; only your output and your file are checked):

```text
$ python cozum.py
Name: Harry
Home: Number Four, Privet Drive
```
