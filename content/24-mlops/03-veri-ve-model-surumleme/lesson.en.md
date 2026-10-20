# Data and Model Versioning

Git keeps every state of the code: you can go back to any commit. But
what about last month's data? The model file that was released three
weeks ago? In the Reproducible Training section we wrote the data
fingerprint into a run's record. But a fingerprint alone doesn't bring
the data back; it only says which data it was. In this section we learn
to **version** data and models like code: keep every state, find it by
name and bring it back.

## Data files

The customer data grows every month. The first version has 4000
customers, the second 5000. Let's write both to CSV files and look at
their sizes and fingerprints:

```python
import hashlib
from pathlib import Path
from ml_data import write_customers_csv


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


write_customers_csv("customers_v1.csv", 4000)
write_customers_csv("customers_v2.csv", 5000)
for name in ["customers_v1.csv", "customers_v2.csv"]:
    print(name, Path(name).stat().st_size, "bytes", file_hash(name))
```

```text
customers_v1.csv 131847 bytes 2448b83141ea
customers_v2.csv 164798 bytes fd8e64e44454
```

This time we computed the fingerprint not from Python objects but from
**the file's bytes**: the hash describes whatever file is on the disk.
The same file gives the same hash on every computer.

## Why not put them straight into Git?

These files are small and could go into Git. But in real projects data
is hundreds of megabytes and model files are big too: the random forest
we will train at the end of this section is 6.9 MB on its
own. Git runs into three problems:

- **History never shrinks.** Git keeps every version. A model retrained
  every week adds more than fifty big files to the repository by the end
  of the year; everyone who clones the repository downloads them all.
- **There are limits.** GitHub does not accept files larger than 100 MB.
- **A diff is useless.** Git shows which line of a text file changed; in
  a binary file such as a model file it can say no more than "changed".

The solution is to split the job in two: big files live in a separate
**store**, and only a small **pointer file** that points at them goes
into Git.

## A content-addressed store

Let each file's name in the store be the hash of its contents. This is
called **content-addressed storage**: you find a file by its contents,
not by its name. The same contents always land in the same place.

```python
import json
import shutil

STORE = Path("store")


def put(path):
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    target = STORE / digest[:2] / digest[2:]
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    pointer = {"path": str(path), "sha256": digest, "size": Path(path).stat().st_size}
    Path(f"{path}.ptr").write_text(json.dumps(pointer, indent=2))
    return digest


put("customers_v1.csv")
print(Path("customers_v1.csv.ptr").read_text())
```

```text
{
  "path": "customers_v1.csv",
  "sha256": "2448b83141eacf2d4a59fe0a808c88c2a2f3c1aba8006c74bd6d58ca77cb8db3",
  "size": 131847
}
```

`put` does three jobs:

1. It computes the file's full hash (64 characters).
2. It copies the file into the store, to a path derived from its hash:
   the first two characters are the folder, the rest the file name.
   Hashes are split like this so that thousands of files don't pile up
   in a single folder.
3. It writes a pointer file (`.ptr`) next to it: which file, what its
   hash is, how many bytes.

The pointer file is a few lines of text. That goes into Git; the CSV
file is written into `.gitignore`. A commit of the code now means "this
code, with this data".

## The same contents are stored once

Let's put the second version into the store too. And let's add a copy of
the first version under another name:

```python
put("customers_v2.csv")
shutil.copyfile("customers_v1.csv", "backup.csv")
put("backup.csv")
pointers = list(Path(".").glob("*.ptr"))
stored = [p for p in STORE.rglob("*") if p.is_file()]
print("pointer files:", len(pointers))
print("files in the store:", len(stored))
```

```text
pointer files: 3
files in the store: 2
```

There are three pointer files but two files in the store. The contents
of `backup.csv` are the same as `customers_v1.csv`, so is the hash; the
place in the store was already taken, so `put` didn't copy a second
time. The contents matter, not the name. (`glob("*.ptr")` lists the
`.ptr` files in the folder, `rglob("*")` everything including
subfolders.)

## Bringing back an old version

With the pointer file in hand, we can bring the data back from the
store. While bringing it back, let's check one more thing: the file in
the store may be damaged (a disk error, an unfinished copy). The hash of
the bytes we bring back must match the one in the pointer file:

```python
def get(pointer_path):
    pointer = json.loads(Path(pointer_path).read_text())
    digest = pointer["sha256"]
    data = (STORE / digest[:2] / digest[2:]).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError(f"{pointer['path']}: the stored file is damaged")
    Path(pointer["path"]).write_bytes(data)


Path("customers_v1.csv").unlink()
print("deleted:", Path("customers_v1.csv").exists())
get("customers_v1.csv.ptr")
print("restored:", file_hash("customers_v1.csv"))
```

```text
deleted: False
restored: 2448b83141ea
```

We deleted the file and brought it back from the pointer file: the
fingerprint is the same as at the start. `unlink` is the `Path` method
that deletes a file. In a real project, whoever calls `get` is someone
going back to an old commit: Git brings back the old pointer file, and
`get` the old data.

## What changed between two versions?

A hash says "changed" but not what changed. If every row of the data has
an identifier (`id`), we can compare two versions row by row:

```python
import csv


def read_rows(path):
    with open(path, encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


old, new = read_rows("customers_v1.csv"), read_rows("customers_v2.csv")
added = [i for i in new if i not in old]
removed = [i for i in old if i not in new]
changed = [i for i in old if i in new and old[i] != new[i]]
print("added:", len(added), "removed:", len(removed), "changed:", len(changed))
print("first new customer:", added[0])
```

```text
added: 1000 removed: 0 changed: 0
first new customer: C00-04001
```

The second version has 1000 new customers; none of the old customers was
deleted or changed. This information is very valuable next to a run
record: when someone says "the model got worse", the first question is
"what changed in the data?". Building the dictionaries as
`{row["id"]: row ...}` lets us find a customer by their identifier at
once.

## Versioning the model

A model is a file too; it goes into the same store. But the model file
alone is not enough: we also want to know which data, which settings and
which library it was trained with. This link from a model back to its
data and code is called **lineage**:

```python
import pickle
import sklearn
from sklearn.ensemble import RandomForestClassifier
from ml_data import NUMERIC


def load(path):
    rows = read_rows(path).values()
    X = [[float(r[c]) for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [int(r["churned"]) for r in rows]
    return X, y


CONFIG = {"n_estimators": 50, "random_state": 0}
model = RandomForestClassifier(**CONFIG).fit(*load("customers_v2.csv"))
Path("model.pkl").write_bytes(pickle.dumps(model))
data_pointer = json.loads(Path("customers_v2.csv.ptr").read_text())
lineage = {
    "model": put("model.pkl")[:12],
    "data": data_pointer["sha256"][:12],
    "config": CONFIG,
    "scikit-learn": sklearn.__version__,
}
print(json.dumps(lineage, indent=2))
```

```text
{
  "model": "dd0ba2458f51",
  "data": "fd8e64e44454",
  "config": {
    "n_estimators": 50,
    "random_state": 0
  },
  "scikit-learn": "1.9.1"
}
```

Every value read from a CSV is text, so it is turned into a number with
`float` and `int`. `RandomForestClassifier(**CONFIG)` unpacks the
dictionary into parameters: the same as writing
`n_estimators=50, random_state=0`.

The lineage record ties the model's identity (its file's hash) to its
data's identity. Six months later the answer to "which data was this
model trained on?" is here; the data is in the store too and comes back
with `get`.

## Same training, same file

In the Reproducible Training section we tested that two models give the
same predictions. Looking at the hashes of the model files, we can run
an even stricter test:

```python
again = RandomForestClassifier(**CONFIG).fit(*load("customers_v2.csv"))
print("same file:", pickle.dumps(again) == Path("model.pkl").read_bytes())
```

```text
same file: True
```

Same data, same settings, same seed: the 6.9 MB file is
identical byte for byte. This is not guaranteed in every library and
every environment (another version or another processor may produce
different bytes); that is why the real test is comparing the
predictions. But when the files come out the same, the store doesn't
keep the same model twice.

A warning about model files: when a file saved with `pickle` is opened,
code inside it can run. Only open model files that you produced yourself
or that come from a source you trust.

## Real tools

The small store we wrote in this section is the same idea as the real
tools:

- **Git LFS** (Large File Storage): a Git extension that keeps big files
  outside Git and puts a pointer file into the repository.
- **DVC** (Data Version Control): writes pointer files (`.dvc`) for data
  and models; it sends the files themselves to a folder or to cloud
  storage. Hash, size and path, as in our `.ptr` file.

Whatever the tool, the rule is the same: the big file in a separate
store, and in Git only a small text that points at it.

## Summary

- Data and models are **versioned** like code: every state is kept and
  can be brought back.
- Big files don't go into Git: history grows, GitHub doesn't accept
  files larger than 100 MB, and a diff is useless on a binary file.
- In a **content-addressed store**, a file's name is the hash of its
  contents. The same contents are stored once.
- A small **pointer file** goes into Git: path, hash, size.
- When bringing a file back, compute the hash again; if it doesn't
  match, the file is damaged.
- Two versions with an identifier column can be compared row by row:
  added, removed, changed.
- A **lineage** record ties a model to its data, settings and
  environment.
