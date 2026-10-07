Servers write every incoming request into a **log**: who asked which
endpoint. These logs answer questions such as "which door is used most?" and
"who keeps asking for a door that does not exist?".

The log is in the `log` list: each item is a `(client, endpoint)` tuple. The
endpoints the API knows are in the `known` list.

**What to do:**

1. Count how many requests each endpoint received in a dictionary called
   `counts`.
2. Print the endpoints **in alphabetical order** as `endpoint count`.
3. Print the total number of requests that went to endpoints not in `known`
   (these get a `404`) as `404 responses: N`.

**Expected output:**

```
/cities 1
/forecast 2
/news 2
/weather 3
404 responses: 2
```
