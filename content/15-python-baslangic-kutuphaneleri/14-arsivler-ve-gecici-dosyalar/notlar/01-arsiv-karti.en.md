## zipfile

| Code | What it does |
|---|---|
| `ZipFile(name, "w", compression=ZIP_DEFLATED)` | write compressed |
| `ZipFile(name, "a")` | append to an existing one |
| `zf.write(file, arcname="folder/name")` | add a file from disk |
| `zf.writestr(name, text)` | write content directly |
| `zf.namelist()` / `zf.infolist()` | names / information |
| `info.file_size`, `info.compress_size` | real / archived size |
| `zf.read(name)` | bytes; `.decode("utf-8")` for text |
| `zf.extract(name, folder)` / `zf.extractall(folder)` | extract |
| `zipfile.is_zipfile(name)` | is it really a zip |

## shutil

| Code | What it does |
|---|---|
| `make_archive(name, "zip", root_dir=folder)` | archive a folder |
| `unpack_archive(file, folder)` | open it, telling the format from the extension |
| `get_archive_formats()` | `zip`, `tar`, `gztar`, `bztar`, `xztar`, `zstdtar` |

## gzip

| Code | What it does |
|---|---|
| `gzip.compress(data)` / `gzip.decompress(data)` | in memory |
| `gzip.open(name, "wt", encoding="utf-8")` | write as text |
| `gzip.open(name, "rt", encoding="utf-8")` | read as text |

## tempfile

| Code | What it gives |
|---|---|
| `TemporaryDirectory()` | a folder deleted when the block ends |
| `NamedTemporaryFile(delete=False)` | a temporary file with a name |
| `mkstemp(dir=..., suffix=...)` | `(handle, name)`: for safe writing |
| `gettempdir()` | the system's temporary folder |

## Rules

- Compression feeds on repetition; small or already compressed files gain
  nothing.
- Open an untrusted archive into an empty, separate folder.
- When writing over the real file, write to a temporary one first, then
  `os.replace`.
