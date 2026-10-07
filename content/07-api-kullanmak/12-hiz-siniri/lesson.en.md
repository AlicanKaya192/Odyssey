# Rate Limits

You cannot send requests to an API as fast as you like. Almost every API sets
a **rate limit**: "60 requests a minute", "3 requests a second", "10,000
requests a day". A client that goes over the limit gets
`429 Too Many Requests` and is made to wait for a while.

The limit is not against you; it is there for everyone. A single client
sending thousands of requests a second slows the server down and spoils the
work of other users. A rate limit protects the server and shares the resource
fairly. Your job is to write a client that **respects** it.

## What happens when you go over?

The practice server's `/limited` endpoint allows 3 requests a second. Let's
send five requests in a row:

```python
import requests

BASE = "http://api.odyssey.test"
for i in range(5):
    r = requests.get(BASE + "/limited")
    left = r.headers.get("X-RateLimit-Remaining")
    print(i + 1, r.status_code, left, r.headers.get("Retry-After"))
# 1 200 2 None
# 2 200 1 None
# 3 200 0 None
# 4 429 0 1
# 5 429 0 1
```

The first three went through; the fourth and fifth got `429`. The responses
tell you the situation at every step:

<figure class="fig">
  <div class="flow">
    <span class="node">Request 1<br><small>200 · 2 left</small></span><span class="arrow">→</span>
    <span class="node">Request 2<br><small>200 · 1 left</small></span><span class="arrow">→</span>
    <span class="node">Request 3<br><small>200 · 0 left</small></span><span class="arrow">→</span>
    <span class="node no">Request 4<br><small>429 · Retry-After: 1</small></span>
  </div>
  <figcaption>The server states your remaining allowance in every response; when it runs out, a 429 comes with how long to wait.</figcaption>
</figure>

## Rate limit headers

Many APIs report your remaining allowance in headers:

- `X-RateLimit-Limit`: the total allowance in the window (3 here).
- `X-RateLimit-Remaining`: what is left. When it hits zero, the next request
  gets `429`.
- `X-RateLimit-Reset`: when the allowance is renewed (in some APIs).
- `Retry-After`: with a `429`, **how many seconds** you must wait.

Header names differ from API to API (`RateLimit-Remaining`,
`X-Rate-Limit-Remaining`...); the documentation says. Names starting with
`X-` are non-standard headers the API sets itself.

## Way 1: wait when a 429 comes

The most basic behaviour: when you get `429`, wait for `Retry-After` and send
**the same request** again.

```python
import time

def get_politely(url):
    while True:
        r = requests.get(url, timeout=5)
        if r.status_code != 429:
            return r
        time.sleep(int(r.headers.get("Retry-After", 1)))
```

If there is no `Retry-After`, wait a sensible default (1 second). In a real
program you would give this loop an upper limit too (Section 11).

`429` is different from the other `4xx` codes: the request is **right**, only
the timing is wrong. So the answer is waiting, not fixing.

## Way 2: set your pace

Better still is never hitting the limit. If you are allowed 3 requests a
second, send the requests **spaced out**:

```python
codes = []
for i in range(6):
    r = requests.get(BASE + "/limited")
    codes.append(r.status_code)
    time.sleep(0.4)          # at most 2.5 requests a second
print(codes)   # [200, 200, 200, 200, 200, 200]
```

With 0.4 seconds between requests we stay under the limit and never get a
`429`. This approach is called **throttling**. The arithmetic is simple: if
the limit is N requests a second, leave at least `1 / N` seconds between
requests; a little margin is wise.

## Way 3: watch the remaining allowance

If the headers tell you what is left, waiting when it reaches zero is another
way:

```python
r = requests.get(BASE + "/limited")
if r.headers.get("X-RateLimit-Remaining") == "0":
    time.sleep(1)            # let the window renew
```

That way you stop exactly when the allowance runs out, without ever getting a
`429`.

## Which one when

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Wait when a 429 comes</h4><p>Easy and works with every API.<br>But you hit the limit; every hit is a wasted request.</p></div>
    <div class="ok"><h4>Set your pace</h4><p>At least <code>1 / N</code> seconds between requests.<br>You never hit the limit.<br>Still keep waiting on 429 as a safety net.</p></div>
  </div>
  <figcaption>A good client uses both together.</figcaption>
</figure>

In practice the two go together: you send requests at a set pace (throttling)
**and** still wait if a `429` comes (a safety net). The limit can change, and
another program may be using the same key; there should always be a safety
net.

## The cost of pushing the limit

APIs can be tougher on clients that keep pushing the limit: longer waits,
temporary bans, even revoking the key. A well-behaved client:

- follows `Retry-After`,
- spaces out its requests,
- sends no unnecessary requests (stores results, leaves filtering to the
  server, asks for big pages),
- accounts for the total rate if several programs use the same key.

## Summary

- APIs set rate limits; a client that goes over gets `429 Too Many Requests`.
- `Retry-After` says how many seconds to wait, `X-RateLimit-Remaining` what
  is left (names vary by API).
- On `429`, **wait and send the same request** again; there is nothing to
  fix.
- Better still, do not hit the limit: leave at least `1 / N` seconds between
  requests (throttling).
- Use pacing and a safety net together; do not send unnecessary requests.
