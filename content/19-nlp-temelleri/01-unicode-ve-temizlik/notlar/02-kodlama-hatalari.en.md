If you see odd letters such as "Ã§alÄ±ÅŸma", the text was read with the
**wrong encoding**. This kind of damage is called **mojibake** (Japanese for
"character jumble").

## How mojibake happens

```python
text = "çalışma"
data = text.encode("utf-8")
print(data)
print(data.decode("cp1254"))
try:
    "çalışma".encode("cp1254").decode("utf-8")
except UnicodeDecodeError as error:
    print(type(error).__name__, error.reason)
print("çalışma".encode("cp1254").decode("utf-8", errors="replace"))
```

```text
b'\xc3\xa7al\xc4\xb1\xc5\x9fma'
Ã§alÄ±ÅŸma
UnicodeDecodeError invalid continuation byte
�al��ma
```

- "ç" is two bytes in UTF-8: `\xc3\xa7`. When those bytes are read with the
  old Turkish Windows encoding (`cp1254`), each byte is taken for a separate
  letter: "Ã§". The file is not damaged; it was only read wrongly. Reading
  it again with the right encoding is enough.
- The reverse is louder: reading bytes written with `cp1254` as UTF-8 raises
  `UnicodeDecodeError`, because those bytes are not valid UTF-8.
- `errors="replace"` puts "�" in place of unreadable bytes and carries on.
  It keeps the program from stopping but does not bring the information
  back; a last resort only.

**Rule:** always state the encoding when opening a file:
`open(path, encoding="utf-8")`. If you leave it out, Python on Windows may
use the system's old encoding, and the same code behaves differently on
another computer.

## BOM: the invisible mark at the start of a file

Some Windows programs put a three-byte mark (a byte order mark, BOM) at the
start of a UTF-8 file.

```python
from pathlib import Path

Path("notes.txt").write_text("hello", encoding="utf-8-sig")
print(Path("notes.txt").read_bytes())
first = Path("notes.txt").read_text(encoding="utf-8")
print(ascii(first), first == "hello")
print(Path("notes.txt").read_text(encoding="utf-8-sig") == "hello")
```

```text
b'\xef\xbb\xbfhello'
'\ufeffhello' False
True
```

Read with `utf-8`, the BOM stays at the start of the text as `\ufeff` and
the first word ("hello") matches nothing. In a CSV file the first column's
name looks broken. The fix: read with `encoding="utf-8-sig"`; it drops the
BOM if there is one and reads plain UTF-8 otherwise.

## A short diagnosis list

| What you see | Cause | Fix |
|---|---|---|
| `Ã§`, `Ä±`, `ÅŸ` | A UTF-8 file read with an old encoding | `encoding="utf-8"` |
| `UnicodeDecodeError` | An old-encoding file taken for UTF-8 | Find the right encoding (`cp1254`, `latin-1`) |
| The first word does not match | A BOM | `encoding="utf-8-sig"` |
| "�" marks | Read earlier with `errors="replace"` | Go back to the source and read it correctly |
