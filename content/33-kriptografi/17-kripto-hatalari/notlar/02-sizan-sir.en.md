When a key, password or token is found to have ended up in a repository,
in logs or in a chat, the order of steps matters.

## Steps

1. **Change it (rotate).** A new secret is made, the systems that use it
   are switched to the new one, and the old one is **revoked**. This is the
   first and most important step.
2. **Clean the record.** It is removed from the file and, if needed, from
   the repository history. This alone is not enough: the repository may
   have been copied, the log may have been read.
3. **Check the impact.** Was the secret used while it was leaked? The
   access logs are reviewed.
4. **Close the cause.** Why did the secret get into the code? A pre-commit
   scanner, environment variables, a secret vault.

## Why change it first

Deleting makes it "invisible", not "unusable". Someone who saw the secret
can still use it after it is deleted. A changed secret, on the other hand,
is no longer good for anything.

## Prevention

| Measure | What it does |
|---|---|
| `.gitignore` | Keeps secret files (`.env`) out of the repository |
| Pre-commit scanner | Catches secrets in quotes before the commit |
| Secret vault | Keeps secrets apart from code, with logged access |
| Short-lived tokens | Shorten the time a leaked token is useful |
| Least privilege | Reduces the doors a leaked secret opens (the Least Privilege and Separation of Duties section) |
