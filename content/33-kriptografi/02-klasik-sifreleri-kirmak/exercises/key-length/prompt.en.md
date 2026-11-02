`vigenere` and `ioc` (it takes a list of letters) are ready. `secret` is
made of lower-case letters only.

`key_length(secret, max_len, threshold)` should split the text into `L`
columns (`secret[i::L]`) for every length `L` from 1 to `max_len`, compute
the average IoC of the columns and return the **first** (smallest) `L`
whose average is equal to or greater than `threshold`. `0` if there is
none.

**Expected output:**

```
5
3
1
```
