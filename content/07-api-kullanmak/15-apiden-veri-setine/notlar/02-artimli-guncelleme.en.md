Fetching only what changed instead of pulling the dataset from scratch every
day.

## The idea

1. Keep the records you have in a dictionary **keyed by identifier**:
   `{id: record}`.
2. Save the last update date in a file (`last_sync.txt`).
3. Ask the API "give me what changed since this date".
4. Write the incoming records into the dictionary: an existing identifier is
   updated, a new one added.
5. Save the new date.

## Code

```python
import json
import os

import requests

BASE = "http://api.odyssey.test"


def read_state():
    if os.path.exists("last_sync.txt"):
        with open("last_sync.txt", encoding="utf-8") as handle:
            return handle.read().strip()
    return "2000-01-01"


def merge(known, changed):
    for book in changed:
        known[book["id"]] = book
    return known


since = read_state()
r = requests.get(BASE + "/changes", params={"since": since}, timeout=10)
changed = r.json()["data"]
with open("books_by_id.json", encoding="utf-8") as handle:
    known = {int(k): v for k, v in json.load(handle).items()}
known = merge(known, changed)
```

Since JSON keys are text (Section 04), we turn them into numbers with
`int(k)` when reading from the file.

## Deleted records

"Give me what changed" endpoints often do not show deleted records. For that,
APIs either offer a separate "deleted" endpoint or add a `deleted: true` field
to the record. If there is neither, you need an occasional full fetch and a
comparison.

## The date format

Keep dates as ISO 8601 text (`2024-03-05`): it is readable, sorts correctly
even as text, and can be compared with `>=`.
