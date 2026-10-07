This Dockerfile works, but the program is root and writes the database to `/app`.

**What to do:**

1. Add `DB_PATH=/data/notes.db` to `ENV`.
2. In a single `RUN`: `useradd --create-home --uid 1000 app`, create the
   `/data` folder and make `app:app` its owner.
3. `USER app` after installing the packages.

Odyssey will run the container **twice** with a volume mounted on `/data` and
look at `/stats`. Because the data stays in the volume, the second time the
program knows it has started twice:

```
{"notes": 0, "starts": 1}
{"notes": 0, "starts": 2}
```
