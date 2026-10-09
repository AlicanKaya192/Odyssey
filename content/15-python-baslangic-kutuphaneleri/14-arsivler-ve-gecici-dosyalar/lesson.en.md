# Archives and Temporary Files

Sending several files as one `.zip`, shrinking a big log file with `.gz`,
opening a downloaded archive, deleting a job's intermediate files without a
trace when it ends... For these the standard library has **`zipfile`**,
**`gzip`**, the archive functions of **`shutil`** and **`tempfile`**. At the
end of the section there is a security point to watch when opening archives.

## zipfile: writing and reading a zip

```python
import zipfile
from pathlib import Path

Path("report.txt").write_text("sales " * 1000, encoding="utf-8")
Path("notes.txt").write_text("short note", encoding="utf-8")
with zipfile.ZipFile("bundle.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write("report.txt")
    zf.write("notes.txt", arcname="docs/notes.txt")
    zf.writestr("readme.txt", "made by Python")
with zipfile.ZipFile("bundle.zip") as zf:
    print(zf.namelist())
    for info in zf.infolist():
        print(info.filename, info.file_size, info.compress_size)
    print(zf.read("docs/notes.txt").decode("utf-8"))
```

```text
['report.txt', 'docs/notes.txt', 'readme.txt']
report.txt 6000 35
docs/notes.txt 10 12
readme.txt 14 16
short note
```

- `ZipFile(name, "w", compression=zipfile.ZIP_DEFLATED)` writes compressed;
  without `compression` the files are stored **uncompressed**.
- `write(file)` adds a file from disk; **`arcname`** sets its name (and
  folder) inside the archive. **`writestr(name, text)`** writes content
  directly, with no file on disk.
- `namelist()` gives the names inside, `infolist()` the information of each:
  `file_size` is the real size, `compress_size` the size in the archive.
- `read(name)` gives the content as **bytes**; for text, `.decode("utf-8")`.

The repetitive text (6000 bytes) went down to 35 bytes. The small files
**grew** (10 → 12 bytes): compression has its own overhead, and a short text
has no repetition to gain from.

## Extracting from an archive

```python
import zipfile
from pathlib import Path

with zipfile.ZipFile("bundle.zip", "w") as zf:
    zf.writestr("readme.txt", "made by Python")
    zf.writestr("docs/notes.txt", "short note")
with zipfile.ZipFile("bundle.zip") as zf:
    zf.extract("readme.txt", "one")
    zf.extractall("all")
print(sorted(p.as_posix() for p in Path("one").rglob("*")))
print(sorted(p.as_posix() for p in Path("all").rglob("*") if p.is_file()))
```

```text
['one/readme.txt']
['all/docs/notes.txt', 'all/readme.txt']
```

`extract(name, folder)` extracts one file, `extractall(folder)` all of them;
the folder structure in the archive (`docs/`) is kept.

## In one line with shutil

```python
import shutil
from pathlib import Path

for name in ["site/index.html", "site/css/style.css"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
archive = shutil.make_archive("site-backup", "zip", root_dir="site")
print(Path(archive).name)
shutil.unpack_archive("site-backup.zip", "restored")
print(sorted(p.as_posix() for p in Path("restored").rglob("*") if p.is_file()))
print([name for name, _ in shutil.get_archive_formats()])
```

```text
site-backup.zip
['restored/css/style.css', 'restored/index.html']
['bztar', 'gztar', 'tar', 'xztar', 'zip', 'zstdtar']
```

Archiving a whole folder is **`shutil.make_archive(name, format,
root_dir=folder)`**, opening it **`shutil.unpack_archive`**. The extension
comes from the format. Besides `zip` there is the `tar` family (`gztar` =
`.tar.gz`); Python 3.14 also brought `zstdtar` with Zstandard compression. If
you need to pick the files one by one, use `zipfile`; for a whole folder,
`shutil`.

## gzip: compressing a single file

```python
import gzip
import random

text = "2026-03-15 INFO request ok\n" * 5000
data = text.encode("utf-8")
packed = gzip.compress(data)
print(len(data), len(packed), round(len(data) / len(packed)))
noise = random.Random(1).randbytes(100_000)
print(len(noise), len(gzip.compress(noise)))
with gzip.open("log.txt.gz", "wt", encoding="utf-8") as f:
    f.write(text)
with gzip.open("log.txt.gz", "rt", encoding="utf-8") as f:
    lines = f.read().splitlines()
print(lines[0], len(lines))
```

```text
135000 397 340
100000 100053
2026-03-15 INFO request ok 5000
```

- **`gzip`** compresses a single file or byte string (`.gz`); log files and
  big CSVs are often stored like this.
- The self-repeating log text shrank **340 times**. Random bytes did not
  shrink at all, they grew a little: compression feeds on repetition, and
  without repetition there is no gain. That is also why already compressed
  files (`.zip`, `.png`, `.mp4`) do not shrink a second time.
- **`gzip.open(name, "wt"/"rt", encoding=...)`** writes and reads a compressed
  file like a plain text file (`t` is text mode). pandas reads `.csv.gz`
  directly too.

## tempfile: temporary files that leave no trace

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    (work / "a.txt").write_text("x", encoding="utf-8")
    print(work.exists(), len(list(work.iterdir())))
print(work.exists())
with tempfile.NamedTemporaryFile(
        "w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("a,b\n")
    name = f.name
print(Path(name).suffix, Path(name).exists())
Path(name).unlink()
print(Path(name).exists(), Path(tempfile.gettempdir()).is_dir())
```

```text
True 1
False
.csv True
False True
```

- **`TemporaryDirectory()`** opens a folder with a unique name in the
  system's temporary folder; when the `with` block ends it **deletes it with
  everything inside**. For a job's intermediate files, tests, archives that
  are downloaded, opened, processed and thrown away.
- **`NamedTemporaryFile`** is a file with a unique name; with `delete=False`
  it is not deleted when the block ends (to hand its name to another
  program), and you delete it yourself later.
- Use these instead of inventing a name by hand (`temp.txt`): two programs
  running at the same time do not overwrite each other's files.

## Security: paths that write outside the archive

```python
import zipfile
from pathlib import Path

with zipfile.ZipFile("evil.zip", "w") as zf:
    zf.writestr("../outside.txt", "gotcha")
with zipfile.ZipFile("evil.zip") as zf:
    print(zf.namelist())
    zf.extractall("safe")
print(Path("../outside.txt").exists())
print(sorted(p.as_posix() for p in Path("safe").rglob("*")))
```

```text
['../outside.txt']
False
['safe/outside.txt']
```

The name of a file in an archive can point **outside the folder**, like
`../outside.txt`; this is called "zip slip", and a malicious archive can try
to overwrite other files on the computer. Python's `zipfile` drops the `..`
parts: the file came out as `safe/outside.txt` and nothing was written
outside. In `tarfile`, the default `filter="data"` since Python 3.14 gives the
same protection. Still, always open an archive you do not trust **into an
empty, separate folder**.

## Summary

- `zipfile.ZipFile(..., "w", compression=ZIP_DEFLATED)`: `write`
  (`arcname`), `writestr`; when reading, `namelist`, `infolist`, `read`,
  `extract`, `extractall`.
- `shutil.make_archive` / `unpack_archive`: a whole folder in one line.
- `gzip.compress` / `gzip.open(..., "rt")`: a single file; it shrinks a lot
  when there is repetition, not at all when there is none.
- `tempfile.TemporaryDirectory()`: a folder deleted when the block ends.
- Open an untrusted archive into an empty folder.
