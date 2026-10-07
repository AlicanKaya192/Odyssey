**What to do:** write two defaults into the image (`ENV`):

1. `APP_ENV=production`
2. `PYTHONUNBUFFERED=1`

Odyssey will also look at the image's settings; on the second run
`-e APP_ENV=test` will be given and you will see `-e` override `ENV`.

**Expected outputs:**

```
env: production
env: test
```
