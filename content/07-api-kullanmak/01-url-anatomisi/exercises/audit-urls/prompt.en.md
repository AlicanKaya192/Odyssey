The addresses a program sent requests to during the day are in the log.
You ask two questions: which ones go **unencrypted** (`http`), and how many
requests went to each computer?

`http` requests to your own computer (`localhost` or `127.0.0.1`) are fine;
the traffic never leaves your machine.

**What to do:**

1. Collect into a list called `insecure` the addresses whose scheme is
   `http` **and** whose host is neither `localhost` nor `127.0.0.1` (keep
   the order).
2. Print `Insecure:`, then each of those addresses on its own line.
3. Print `Requests per host:`, then each host and its number of requests,
   **sorted** by host name.

**Expected output:**

```
Insecure:
http://api.example.com/v1/login?user=ada
http://data.example.org/export?format=csv
Requests per host:
127.0.0.1 1
api.example.com 2
api.github.com 1
data.example.org 1
localhost 1
```
