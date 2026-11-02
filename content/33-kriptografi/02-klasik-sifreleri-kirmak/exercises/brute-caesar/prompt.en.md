`caesar` is ready. `brute_caesar(secret, common)` should decrypt
`caesar(secret, -s)` for every shift `s` from 0 to 25 and count how many of
its words are in the `common` list. Return the shift with the most hits as
`[shift, plaintext]`; on a tie the **smaller** shift wins.

**Expected output:**

```
[3, 'the secret is in the garden']
[7, 'the book is on the table']
```
