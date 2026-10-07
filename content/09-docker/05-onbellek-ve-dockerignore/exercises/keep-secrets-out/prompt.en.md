The Dockerfile copies everything with `COPY . .`; the key in `.env` goes
into the image too.

**What to do:** write `.env` and `notes.txt` in the `.dockerignore` file.
Odyssey will build the image and check that these two files are **not**
inside it.

`app.py` prints the files in the working folder. **Expected output:**

```
files: ['.dockerignore', 'Dockerfile', 'app.py']
```

(`.dockerignore` and `Dockerfile` went into the image too; you could leave
them out as well, but in this exercise this is the expected output.)
