# File Traps

Mistakes with files are expensive: most of them raise no error and quietly
**lose data**. These are the ones people hit most often.

## 1. `"w"` wipes the file

This is the costliest trap.

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("new line\n")
```

If `results.txt` held a month of records, they are gone. `"w"` empties the
file the moment it opens it — before you have even called `write`.

If you are adding to a file, use `"a"`:

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("new line\n")
```

If you are not sure, use `"x"`; it refuses to write when the file exists:

```python
try:
    with open("results.txt", "x", encoding="utf-8") as file:
        file.write("new line\n")
except FileExistsError:
    print("file already exists, not overwriting")
```

## 2. Reading a file twice

This behaviour raises no error but surprises everyone:

```python
with open("notes.txt", encoding="utf-8") as file:
    first = file.read()
    second = file.read()

print(len(first))
print(len(second))
```

```
28
0
```

The second one is empty. The reason: a file has a **read position**. `read()`
moves it all the way to the end; the second `read()` starts at the end and
finds nothing left to read.

The fix: read once, keep it in a variable.

```python
with open("notes.txt", encoding="utf-8") as file:
    content = file.read()

lines = content.splitlines()
words = content.split()
```

The same applies after a `for line in file:` loop — once the loop finishes,
the position is at the end.

## 3. Forgetting `\n`

```python
with open("names.txt", "w", encoding="utf-8") as file:
    file.write("Ada")
    file.write("Alan")
```

The contents of the file:

```
AdaAlan
```

`write` adds no line break. You get used to `print` adding one.

```python
    file.write("Ada\n")
    file.write("Alan\n")
```

If you are writing a list you can do it in one line:

```python
names = ["Ada", "Alan", "Grace"]

with open("names.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(names) + "\n")
```

## 4. Forgetting `strip()`

```python
with open("names.txt", encoding="utf-8") as file:
    for line in file:
        if line == "Ada":
            print("found")
```

It prints nothing. The line read is `"Ada\n"`, and what you compared it to is
`"Ada"`.

```python
        if line.strip() == "Ada":
```

The same trap exists when converting to a number — but there you are lucky:
`int("42\n")` works, because `int` strips whitespace itself. So does `float`.
String comparison offers no such convenience.

## 5. Leaving out `encoding`

```python
with open("notes.txt", encoding="utf-8") as file:
```

Without it, Python uses the operating system's default encoding. On a Windows
machine set to Turkish that is usually `cp1254`; on Linux it is `utf-8`.

The result: a file that opens fine on your machine raises a
`UnicodeDecodeError` on someone else's, or the letters come out broken.

**Write it in every `open` call.** Ten extra characters, and you never have to
think about it again.

## 6. Relative paths

```python
open("data.txt")
```

This file is looked for **in the folder the program runs in** — not in the
folder the code file sits in. Those two can be different.

When you run `python scripts/main.py` from a terminal, Python looks for
`data.txt` in the folder you are standing in, not in `scripts/`.

If you want to be sure, build the path relative to the code file:

```python
from pathlib import Path

folder = Path(__file__).parent
with open(folder / "data.txt", encoding="utf-8") as file:
    content = file.read()
```

## 7. Not using `with`

```python
file = open("notes.txt", "w", encoding="utf-8")
file.write("hello")
# close was never called
```

What you write does not go straight to disk; Python keeps a buffer and flushes
it when the file closes. If `close()` is never called, the data can sit in the
buffer.

If the program ends normally Python usually cleans up. But if an error gets in
the way, or the program runs for a long time, you lose data.

`with` makes this something you never have to think about.

## 8. Switching from reading to writing

```python
with open("notes.txt", "r", encoding="utf-8") as file:
    file.write("hello")
```

```
io.UnsupportedOperation: not writable
```

The mode means what it says. A file opened for reading cannot be written to.
If you need to do both, write two separate blocks — read, close, then write:

```python
with open("notes.txt", encoding="utf-8") as file:
    lines = file.read().splitlines()

lines.append("new line")

with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")
```

## Summary

| Trap | What happens |
|---|---|
| Opening with `"w"` | The old contents are deleted |
| Calling `read()` twice | The second one comes back empty |
| Forgetting `\n` | Everything lands on one line |
| Forgetting `strip()` | Comparisons never match |
| Leaving out `encoding` | It breaks on another machine |
| Relative paths | The file is not found |
| Not using `with` | Data may never reach the disk |
| The wrong mode | `UnsupportedOperation` |
