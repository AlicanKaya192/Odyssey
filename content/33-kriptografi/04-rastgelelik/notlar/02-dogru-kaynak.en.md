## Common mistakes

| Mistake | Why is it a problem? | The right way |
|---|---|---|
| Making a token with `random` | The generator is not cryptographic; its output is predictable | `secrets.token_urlsafe(32)` |
| Taking the seed from the clock | The clock is a predictable value | No seed at all; use `secrets` |
| A fixed seed (`random.seed(1)`) | The same values on every run | Only in tests and simulations |
| `byte % n` | Modulo bias: some results come out more often | `secrets.randbelow(n)` |
| A short token | Few bits; few tries are enough | At least 128 bits |
| Writing your own generator | Looks random but has not been studied | The operating system's source |
| Reusing the same nonce | Like key reuse in stream ciphers | A new nonce for every message |

## Where is `random` the right tool?

- Simulations and experiments: repeating the result with the same seed is
  a feature.
- Games, a shuffled question order, sampling.
- Making test data.

The test is a single question: **if someone predicts this value, does any
harm follow?** If the answer is yes, `secrets`.

## What to look for in code review

- Names like `token`, `key`, `salt`, `nonce`, `password`, `session`,
  `reset` in a file that has `import random`.
- A `random.seed(...)` call and the value given to it (especially the
  clock).
- Random bytes brought into a range with `% n`.
- Token length: how many bytes, how many bits?
- `random.SystemRandom` is safe (it uses the same operating system
  source); it raises a false alarm only because of its name.

## Layer the defence

The right source alone does not solve everything:

- Short verification codes (for example six digits, about 20 bits) get a
  limit on tries and expire within a few minutes.
- A token is deleted once it has been used.
- Tokens are compared with a constant-time comparison
  (`secrets.compare_digest`, the Message Authentication: HMAC section).
