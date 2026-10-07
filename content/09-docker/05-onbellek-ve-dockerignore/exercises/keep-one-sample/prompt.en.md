The `data` folder has a large export (`full_export.csv`) and a small sample
(`sample.csv`). The program only uses the sample.

**What to do:** write two lines in `.dockerignore`:

1. Leave out the `data` folder.
2. But let `data/sample.csv` in anyway: an **exception** to the previous
   rule starts with `!`.

**Expected output:**

```
rows: 3
data files: ['sample.csv']
```
