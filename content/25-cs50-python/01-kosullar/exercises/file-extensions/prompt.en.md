Most file names end with an **extension**, a suffix starting with a period: GIFs end with `.gif`, JPEGs with `.jpg` or `.jpeg`. Web browsers instead rely on **media types** (formerly MIME types) to know how to display a file: `image/gif` for a GIF, `image/jpeg` for a JPEG.

Implement a program that prompts the user for the name of a file and outputs its media type if the name ends, case-insensitively, in any of these suffixes:

- `.gif` → `image/gif`
- `.jpg`, `.jpeg` → `image/jpeg`
- `.png` → `image/png`
- `.pdf` → `application/pdf`
- `.txt` → `text/plain`
- `.zip` → `application/zip`

If the name ends with some other suffix or has no suffix at all, output `application/octet-stream`. (In CS50 the file is `extensions.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `happy.jpg` → output `image/jpeg`
- Input `document.pdf` → output `application/pdf`
- Input `Photo.PNG` → output `image/png`
- Input ` notes.txt ` → output `text/plain`
- Input `cat.gif` → output `image/gif`
- Input `picture.jpeg` → output `image/jpeg`
- Input `archive.ZIP` → output `application/zip`
- Input `page.html` → output `application/octet-stream`
- Input `README` → output `application/octet-stream`
