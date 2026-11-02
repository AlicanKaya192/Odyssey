The question to ask before starting is not "which algorithm?" but **"what
do I want to protect?"**. Mixing up the words is the most common mistake.

## What do you need?

| Need | Right tool | Wrong choice |
|---|---|---|
| Nobody may read it | Encryption | Base64 ("nobody can read it anyway") |
| I want to notice if it is changed | HMAC (shared key) or a signature | A plain hash alone: the attacker changes the data and recomputes the hash too |
| Store a password | A salted, slow password hash | Encryption (whoever gets the key opens them all) or a plain hash |
| Prove to a third party who sent it | Digital signature | HMAC (both sides know the key, so either could have made it) |
| A random token or key | `secrets`, `os.urandom` | `random` (predictable) |

## Three questions

1. **Does it need to be reversed?** If not, a hash; if so, encryption.
2. **Who will reverse it?** If only those who know the key, encryption; if
   everyone, encoding (not security).
3. **Who needs proof?** If only the two sides, HMAC; if a third party, a
   signature.

## Rules

- Use a high-level, well-tested library; do not assemble low-level pieces
  yourself.
- Do not write keys into code; read them from configuration or a secrets
  vault.
- Remember that what you keep secret is the **key**, not the algorithm's
  name.
