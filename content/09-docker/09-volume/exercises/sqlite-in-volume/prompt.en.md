Every time `visits.py` runs, it adds a visit to an SQLite database and
prints the total. It reads the database's location from the `DB_PATH`
environment variable; otherwise it writes to the working folder (`app.db`)
and the data is reset in every container.

**What to do:**

1. Write the default `DB_PATH=/data/visits.db` with `ENV`.
2. Document `/data` with `VOLUME`.

Odyssey will run two separate containers with the same volume
(`-v visits:/data`).

**Expected outputs:**

```
db: /data/visits.db visits: 1
db: /data/visits.db visits: 2
```
