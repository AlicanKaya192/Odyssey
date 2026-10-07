`notes.py` appends the text it is given to `/data/notes.txt` and prints the
total number of notes.

**What to do:**

1. Document with `VOLUME` that the data lives in `/data`.
2. With `ENTRYPOINT`, `python notes.py` should always run (the note will come
   as an argument).

Odyssey will run two **separate** containers, mounting the same volume on
both (`-v notes:/data`): one adds the note `buy milk`, the other `call Ada`.

**Expected outputs:**

```
notes: 1
notes: 2
```
