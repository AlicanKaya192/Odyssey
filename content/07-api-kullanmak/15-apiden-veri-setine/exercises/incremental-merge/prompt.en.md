The dataset you fetched yesterday is in `known.json` (identifier → record), and
the last update date is in `last_sync.txt`. Today, fetch only what changed
and merge it.

**What to do:**

1. Read `last_sync.txt`; read `known.json` and put it into a `known`
   dictionary, turning the keys into **numbers**.
2. Get the changes with `GET /changes?since=<date>`.
3. Write each changed record into `known`: count it as `updated` if the
   identifier exists, otherwise `added`.
4. Print the changed identifiers, how many were updated and added, the number
   of records in `known` and the new last update date (the largest `updated`
   among the changes).

**Expected output:**

```
changed: [6, 10, 13, 20, 23]
updated: 4 added: 1
records: 21
new last sync: 2024-03-14
```
