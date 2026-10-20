How big files are versioned:

| Where | What lives there | Why |
|---|---|---|
| Git | Code, pointer files (`.ptr`, `.dvc`), `.gitignore` | Small text; every commit says "this code, this data" |
| The store | The data and model files themselves | Big and binary; their history shouldn't bloat Git |
| `.gitignore` | The names of the big files | So they don't end up in Git by mistake |

## The pointer file

```text
{
  "path": "customers_v1.csv",
  "sha256": "<a 64-character hash>",
  "size": 131847
}
```

- `path`: where the file is written when it is brought back.
- `sha256`: its place in the store and the integrity check.
- `size`: a quick first check; if the size doesn't match, there's no
  need to compute the hash.

## The path in the store

If the hash is `2448b8...`, the file is at `store/24/48b8...`: the first
two characters are the folder, the rest the name. The same contents
always land on the same path, so they are never copied twice.

## Operations

| Operation | What it does |
|---|---|
| `put(path)` | Compute the hash, copy the file into the store (if missing), write the pointer file |
| `get(pointer)` | Read from the store, compute the hash again, write the file if it matches |
| Diff | Count the added, removed and changed rows by the identifier column |

## Their counterparts in real tools

| In this section | DVC | Git LFS |
|---|---|---|
| `put("data.csv")` | `dvc add data.csv` | `git lfs track "*.csv"` + `git add` |
| The `.ptr` file | The `.dvc` file | The pointer text in Git |
| The store folder | `.dvc/cache` + a remote (`dvc push`) | The LFS server |
| `get(...)` | `dvc pull`, `dvc checkout` | `git lfs pull` |

## Terms

- **Versioning:** keeping every state of something and being able to
  bring it back by name.
- **Content-addressed storage:** naming and storing a file by the hash of
  its contents.
- **Pointer file:** a small text that holds a big file's path, hash and
  size.
- **Binary file:** a file that is not text, such as a model file.
