Even in the most careful team, a secret leaks one day: a configuration file
pushed to the repository by mistake, a terminal visible during screen
sharing, a key that ends up in an error message. What matters is not only
that leaks do not happen, but that what to do when one happens is known in
advance.

## When a leak is noticed

1. **Rotate, then clean.** The first job is generating a new value, moving
   the systems to it and **revoking** the old value. Deleting it from the
   repository or the history is the second job; the value may already have
   been copied.
2. **Set the scope.** What did the secret give access to? Which systems,
   which data? When did the leak happen, when was it noticed?
3. **Check whether it was used.** Accesses made with that secret since the
   leak are searched for in the logs (the Logging and Monitoring section).
   If there is an unexpected access, incident response begins (the
   Incident Response section).
4. **Fix the root.** Why did the secret end up there? A lasting measure is
   taken, such as a `.gitignore` line, a pre-commit scan, or moving the
   secret into the vault.

## To prevent it

| Measure | What does it catch? |
|---|---|
| Pre-commit secret scanning | A secret before it enters the repository |
| Secret scanning in the build pipeline | Secrets that slipped through |
| Keeping secret files out with `.gitignore` | `.env`, key files |
| Redaction in logs | Secrets in debug lines |
| Short-lived secrets | How long a leaked value stays valid |
| Least-privilege secrets | The doors a leaked secret can open |

## The least-privilege secret

A secret should give only the privilege the job needs: the database user
of an application that reads reports cannot write; a key that uploads to
only one folder cannot touch other folders. That way, when a leak happens,
the damage stays limited to the small area the secret can open.

## Sharing a secret

When a secret has to be given to a teammate, email, chat or documents are
not used: these get copied and kept for years. The right way is giving the
person access in the secrets vault, or using a sharing method that can be
opened once and expires.
