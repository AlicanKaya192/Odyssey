If the program is interrupted while writing over a settings or data file
(the power goes, the program crashes), the file is left **half-written**: the
old content is gone and the new one is incomplete. The common fix is to
**write to a temporary file first and then swap it in**.

```python
import os
import tempfile
from pathlib import Path


def atomic_write(path, text, crash=False):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        if crash:
            raise RuntimeError("power cut")
        os.replace(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


settings = Path("settings.json")
settings.write_text('{"theme": "dark"}', encoding="utf-8")
with open(settings, "w", encoding="utf-8") as f:
    f.write('{"the')
print(settings.read_text(encoding="utf-8"))
settings.write_text('{"theme": "dark"}', encoding="utf-8")
try:
    atomic_write(settings, '{"theme": "light"}', crash=True)
except RuntimeError:
    print("crashed")
print(settings.read_text(encoding="utf-8"))
atomic_write(settings, '{"theme": "light"}')
print(settings.read_text(encoding="utf-8"))
print(sorted(p.name for p in Path(".").glob("*.tmp")))
```

```text
{"the
crashed
{"theme": "dark"}
{"theme": "light"}
[]
```

- The first attempt shows the problem with writing directly:
  `open(..., "w")` **empties the file as soon as it opens it**; when the
  write stopped halfway, `{"the` was left, not even valid JSON.
- **`atomic_write`** writes the new content to a temporary file in the same
  folder (`mkstemp` gives a unique name). If something happens before the
  write finishes (`crash=True`), the real file has **never been touched**:
  `{"theme": "dark"}` is still there.
- When the write is done, **`os.replace(temporary, real)`** puts the
  temporary file in place of the real one. On the same disk this is a single
  step: anyone reading the file sees either the old one or the new one, never
  a half.
- `finally` cleans up the temporary file in every case; no `.tmp` is left in
  the folder.
- The temporary file is opened **in the same folder**: `os.replace` cannot be
  a single step when moving to another disk.

This pattern is used for settings files, caches and progress records.
