`bucket(user_id, salt)` should take the MD5 hash of the text
`f"{salt}:{user_id}"` (`hashlib.md5(...).hexdigest()`), turn it into a
number in base 16 and return the remainder of dividing by 100. The starter
code sums character codes; similar ids land in similar buckets.

**Expected output:**

```text
41
60
```
