The program that sent the request wrote the header names in different
ways: `Host`, `ACCEPT`, `user-agent`. Since header names are not
case-sensitive, the program should store them all **lower-cased**.

**What to do:**

1. Split `raw` into lines. The first line is the request line; the rest are
   headers.
2. Store the headers in a dictionary called `headers`, **with lower-case
   names**. Split each value only at the **first** `": "` separator (the
   `Host` value contains a colon too).
3. Print the host, the `Accept` value and whether the request carries an
   `Authorization` header, as below.

**Expected output:**

```
host: localhost:8000
accept: application/json
has authorization: False
```
