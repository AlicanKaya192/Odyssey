Next to your file there is an `inbox` folder: `photo.jpg`, `report.pdf`,
`data.csv`, `notes.txt`, `scan.PDF`, `README`.

Write the function `organize(folder)`: move every **file** in the folder into
a subfolder named after its extension in lowercase without the dot
(`scan.PDF` → `pdf/`); with no extension, `other/`. At the end return the
relative, `/`-separated paths of all files in the folder as a **sorted**
list. Called a second time it must give the same list without moving
anything.

**Expected output:**

```
csv/data.csv
jpg/photo.jpg
other/README
pdf/report.pdf
pdf/scan.PDF
txt/notes.txt
```
