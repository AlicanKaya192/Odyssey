There is a `photos` folder next to your file. Turn names given by a phone,
like `IMG_20260315_101500.jpg`, into the form `2026-03-15_10-15-00.jpg`.

Write the function `rename_photos(folder)`: for every file whose name
**fully** matches the pattern `IMG_(\d{8}_\d{6})\.jpg`, read the date with
`datetime.strptime(..., "%Y%m%d_%H%M%S")`, build the new name with
`strftime("%Y-%m-%d_%H-%M-%S")` and `rename` it. Leave the others alone. At
the end, return the names in the folder sorted.

**Expected output:**

```
2026-03-15_10-15-00.jpg
2026-03-16_08-30-12.jpg
IMG_bad.jpg
notes.txt
```
