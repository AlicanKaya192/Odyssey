# Working with Files

Every program you have written so far ended the same way: the program closed
and everything vanished. Variables live in memory, and memory is cleared when
the program ends.

For something to last, it has to be written to **disk**. That is what this
section is about: opening, reading and writing files without losing data
along the way.

This matters especially in data science. The data you work with comes from a
file, and what pandas does first is exactly this.

## Opening a file

The right way to open a file is with `with`:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("first line\n")
```

There are three parts:

<figure class="fig anat">
  <div class="sig">open(<u class="m1">"notes.txt"</u>, <u class="m2">"w"</u>, <u class="m3">encoding="utf-8"</u>)</div>
  <ul class="legend">
    <li class="m1"><b>The file name</b> — which file. Without a path it is looked for in the folder the program runs in.</li>
    <li class="m2"><b>The mode</b> — what you are going to do. <code>"w"</code> write, <code>"r"</code> read, <code>"a"</code> append.</li>
    <li class="m3"><b>The encoding</b> — how letters are written to disk. Always write <code>utf-8</code>.</li>
  </ul>
</figure>

## Why `with`?

A file you open has to be closed. `with` does that for you:

<figure class="fig">
  <div class="flow">
    <span class="node acc">the <b>with</b><br>block starts</span>
    <span class="arrow">→</span>
    <span class="node">the file opens</span>
    <span class="arrow">→</span>
    <span class="node">you do your work</span>
    <span class="arrow">→</span>
    <span class="node ok">it closes <b>on its own</b><br>when the block ends</span>
  </div>
  <figcaption>The file closes even if an error comes up inside the block. Opening and closing by hand gives you no such guarantee.</figcaption>
</figure>

You can do it by hand, but nobody does:

```python
file = open("notes.txt", "w")
file.write("hello")
file.close()          # if you forget this, the data may never reach the disk
```

If an error comes up in between, the `close()` line is never reached and what
you wrote may not have made it to disk. `with` removes that problem entirely.

## Writing

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("first line\n")
    file.write("second line\n")
```

Two things to watch for:

**`write` does not add a line break.** `print` moves to the next line on its
own; `write` does not. If you do not write `\n`, everything ends up on one
line.

**The `"w"` mode wipes the file.** If the file exists, its contents are gone
and it is written from scratch.

## The difference between `"w"` and `"a"`

Not knowing this difference leads to real data loss:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>"w" — WRITE FROM SCRATCH</h5>
<pre><code>with open("log.txt", "w") as f:
    f.write("new\n")</code></pre>
    </div>
    <div class="ok">
      <h5>"a" — APPEND</h5>
<pre><code>with open("log.txt", "a") as f:
    f.write("new\n")</code></pre>
    </div>
  </div>
  <figcaption>The left-hand one deletes the file's old contents. The right-hand one keeps them and adds to the end. If you are keeping a log, you want the one on the right.</figcaption>
</figure>

## Reading

There are three ways, each good for something different.

**The whole thing as one string:**

```python
with open("notes.txt", encoding="utf-8") as file:
    content = file.read()

print(content)
```

When you write no mode, the default is `"r"` — reading. That is why `"r"` is
usually left out.

**As a list of lines:**

```python
with open("notes.txt", encoding="utf-8") as file:
    lines = file.read().splitlines()

print(lines)
```

```
['first line', 'second line']
```

`splitlines()` splits and strips the line endings as it goes, which makes it
the preferred way.

**Going line by line:**

```python
with open("notes.txt", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

This third one has an important advantage: it does not pull the whole file
into memory, it reads line by line. With small files it makes no difference,
but with a two-gigabyte data file it is the only workable way.

## Watch the line endings

Every line read from a file has a `\n` at the end:

```python
with open("notes.txt", encoding="utf-8") as file:
    for line in file:
        print(repr(line))
```

```
'first line\n'
'second line\n'
```

`strip()` removes whitespace from both ends, including the line ending:

```python
clean = line.strip()
```

Forgetting this causes a sneaky bug: the comparison `line == "first line"`
comes out `False`, because the right-hand side has no `\n`.

## Modes

| Mode | What it does | If the file does not exist |
|---|---|---|
| `"r"` | Reads (the default) | `FileNotFoundError` |
| `"w"` | Writes from scratch, deleting the old contents | Creates it |
| `"a"` | Appends to the end | Creates it |
| `"x"` | Writes, but fails if the file exists | Creates it |

The `"x"` mode is little known but useful: it makes overwriting by accident
impossible.

## Why does `encoding` matter?

Letters are written to disk as numbers. Which letter becomes which number is
decided by the **encoding**.

If you do not write `utf-8`, Python uses the operating system's default, and
on Windows that can differ. The result: a file you wrote on one machine looks
broken on another, or you get a `UnicodeDecodeError`.

**Rule: write `encoding="utf-8"` in every `open` call.** No exceptions.

## When the file is not there

Trying to read a file that does not exist raises an error:

```python
with open("missing.txt", encoding="utf-8") as file:
    content = file.read()
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

The `try` / `except` from the previous section fits exactly here:

```python
try:
    with open("settings.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    content = ""
    print("no settings file, using defaults")
```

Catching it is meaningful here: you fall back to a default.

## Reading a simple data file

The shape you will meet most often in data science is fields separated by
commas on each line:

```
Ada,90
Alan,70
Grace,85
```

Reading it brings together everything you have learned:

```python
scores = {}

with open("scores.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        name, value = line.split(",")
        scores[name] = int(value)

print(scores)
```

```
{'Ada': 90, 'Alan': 70, 'Grace': 85}
```

Read line by line, clean it, skip the empty line, split, convert, put it in
the dictionary. That is what the `read_csv` function in pandas does at heart —
only with a great deal more detail.

## Summary

- Variables disappear when the program ends; anything that has to last gets
  written to a file.
- **Always** open files with `with`; they close on their own when the block
  ends.
- `open(name, mode, encoding="utf-8")` — write the encoding every time.
- `"r"` reads, `"w"` writes **after deleting the old contents**, `"a"`
  appends, `"x"` refuses to write if the file exists.
- `write` adds no line break; you have to write `\n` yourself.
- Lines read from a file end with `\n`; clean them with `strip()`.
- Read the whole file with `read()`, a list of lines with
  `read().splitlines()`, and large files with `for line in file:`.
- A missing file raises `FileNotFoundError`; catch it with `try` / `except`
  when you have a meaningful response.
