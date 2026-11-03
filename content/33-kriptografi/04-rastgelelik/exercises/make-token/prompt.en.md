`make_token(length, alphabet)` should make a random token of `length`
characters from the characters in the alphabet. Choose the characters
with `secrets.choice`.

Because the token's value changes on every run, the code below prints its
**properties**, not its values: the length, the alphabet, all 100 tokens
being different, and on the last line the effect of the seed. The
starter code's `random.choices` gives the same token with the same seed;
`secrets` is not affected by the seed.

**Expected output:**

```
lengths ok: True
alphabet ok: True
all different: True
seed has no effect: True
```
