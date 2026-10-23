Everything from week 6 on one page.

## Opening a file

| Code | What it does |
|---|---|
| `open("names.txt")` | opens for reading (`"r"` is the default) |
| `open("names.txt", "w")` | opens for writing; if the file exists, **empties it** |
| `open("names.txt", "a")` | opens for appending; creates the file if missing |
| `with open(...) as file:` | closes the file by itself when the block ends |
| `file.close()` | to close it when you are not using `with` |

## Writing and reading

| Code | What it does |
|---|---|
| `file.write(f"{name}\n")` | writes the text; **you** add the line ending |
| `file.readlines()` | every line, as a list (each ends in `\n`) |
| `for line in file:` | walks the file line by line |
| `line.rstrip()` | removes whitespace and `\n` on the right |
| `sorted(file)` | gives the lines in order |

## Sorting

| Code | What it does |
|---|---|
| `sorted(names)` | alphabetical (capitals first: `"C"` before `"a"`) |
| `sorted(names, reverse=True)` | reverse order |
| `sorted(students, key=get_name)` | by the value of `get_name(item)` for each item |
| `key=lambda s: s["name"]` | the same, with a nameless function |

`sorted` is stable: items with equal values (two students in the same
house) keep their order from the input.

## CSV

With `import csv`:

| Code | What it does |
|---|---|
| `csv.reader(file)` | each row is a **list**; quoted fields are read correctly |
| `csv.DictReader(file)` | the first row is a header; each row is a **dict** (`row["name"]`) |
| `csv.writer(file)` | `writer.writerow([name, home])` |
| `csv.DictWriter(file, fieldnames=[...])` | `writer.writerow({...})`; the column order comes from `fieldnames` |
| `writer.writeheader()` | writes a `DictWriter`'s header row |

On Windows, open a CSV you write with `open("students.csv", "a",
newline="")`; otherwise blank lines appear between the rows.

## Images (Pillow)

With `from PIL import Image`:

| Code | What it does |
|---|---|
| `Image.open("costume1.gif")` | opens an image |
| `image.size` | `(width, height)` |
| `image.save("out.png")` | saves it, picking the format from the extension |
| `images[0].save("x.gif", save_all=True, append_images=images[1:], duration=200, loop=0)` | an animated GIF |
| `ImageOps.fit(image, size)` | resizes the image and crops it from the center (`from PIL import ImageOps`) |
| `photo.paste(shirt, shirt)` | puts `shirt` on top; the second one is the transparency mask |
