# Errors, Timeouts and Retries

So far every request went well: the server was up, answered fast and the
connection held. Real life is not like that. The server is under maintenance
or overloaded, the network drops for a moment, the response never comes. The
real test of a program that works with an API is what it does when things go
wrong.

In this section you learn three things: setting a **timeout**, catching
errors **by kind**, and **retrying wisely** on temporary errors.

## Two kinds of error

Working with an API you meet two separate kinds of problem:

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>A response, but bad news</h4><p><code>404</code>, <code>500</code>, <code>503</code>...<br>The connection worked, the server spoke.<br>requests raises nothing; <b>you look at the code</b> or call <code>raise_for_status()</code>.</p></div>
    <div class="no"><h4>No response at all</h4><p>A timeout, no connection.<br>There is no server to talk to.<br>requests <b>raises an exception</b>; you catch it with <code>try</code>/<code>except</code>.</p></div>
  </div>
  <figcaption>Telling the two apart decides what to do in each case.</figcaption>
</figure>

- **A response came, but bad news:** `404`, `500`, `503`. The connection
  worked and the server spoke. requests does not count these as errors
  (Section 06); you look at the code.
- **No response came:** the server could not be reached or did not answer in
  time. Here requests raises an **exception**; if you do not catch it, the
  program stops.

## Timeouts: give every request a limit

By default requests **waits for ever.** If the server does not answer, your
program freezes. So the golden rule: **give every request a `timeout=`.**

```python
import requests

BASE = "http://api.odyssey.test"
try:
    requests.get(BASE + "/slow", timeout=1)
except requests.Timeout as error:
    print("Timeout:", type(error).__name__)   # Timeout: ReadTimeout
```

The practice server's `/slow` endpoint answers after 3 seconds; the request
willing to wait 1 second raised `requests.Timeout`. With a longer limit the
answer arrives:

```python
r = requests.get(BASE + "/slow", timeout=5)
print(r.status_code)   # 200
```

How many seconds? It depends on the job; 5–10 seconds is a common start.
What matters is **setting** a value.

## Connection errors

If the server cannot be reached at all (the name cannot be resolved, the
machine is off, there is no network), you get `requests.ConnectionError`:

```python
try:
    requests.get("http://offline.odyssey.test/books", timeout=3)
except requests.ConnectionError as error:
    print("ConnectionError:", type(error).__name__)
```

## The exception family

requests' errors are a family: they all derive from
`requests.RequestException`.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>RequestException</code></span><span>The ancestor of them all: "a problem with the request"</span></div>
    <div class="anat-row"><span>├ <code>Timeout</code></span><span>No response in time (<code>ConnectTimeout</code>, <code>ReadTimeout</code>)</span></div>
    <div class="anat-row"><span>├ <code>ConnectionError</code></span><span>The server could not be reached</span></div>
    <div class="anat-row"><span>├ <code>HTTPError</code></span><span><code>raise_for_status()</code> saw a 4xx/5xx</span></div>
    <div class="anat-row"><span>└ <code>JSONDecodeError</code>, <code>MissingSchema</code>...</span><span>Others</span></div>
  </div>
  <figcaption><code>except requests.RequestException</code> catches them all; write the specific ones first and you can respond to each separately.</figcaption>
</figure>

That gives you choices when catching them:

```python
try:
    r = requests.get(BASE + "/books/1", timeout=5)
    r.raise_for_status()
except requests.Timeout:
    print("too slow")
except requests.ConnectionError:
    print("cannot reach the server")
except requests.HTTPError:
    print("bad status:", r.status_code)
except requests.RequestException as error:
    print("other request problem:", error)
```

Write them from specific to general: `Timeout` first, then
`ConnectionError`, and the catch-all `RequestException` last. In the reverse
order the general one catches everything and the specific cases never get a
turn.

## Which errors are retried?

Retrying only helps with **temporary** problems. The rule from Section 03
turns into a decision here:

| Situation | Temporary? | Retry? |
|---|---|---|
| `Timeout`, `ConnectionError` | Usually | Yes |
| `500`, `502`, `503`, `504` | Usually | Yes |
| `429` | Yes | Yes, but after waiting for `Retry-After` (Section 12) |
| `400`, `401`, `403`, `404`, `422` | No | **No**: fix the request |

And the warning from Section 02: a retried request must be **idempotent**.
`GET`, `PUT` and `DELETE` are safe to repeat; sending a `POST` again may
create duplicate records.

## A simple retry

The practice server's `/flaky` endpoint answers `503` (busy) to the first two
requests and answers properly on the third:

```python
import time

for attempt in range(1, 6):
    r = requests.get(BASE + "/flaky", timeout=5)
    print("attempt", attempt, r.status_code)
    if r.status_code == 200:
        break
    time.sleep(1)
# attempt 1 503
# attempt 2 503
# attempt 3 200
```

There are three important parts:

1. **An upper limit:** `range(1, 6)` is at most 5 attempts. Endless retries
   push the problem onto the server.
2. **Waiting:** `time.sleep(1)`. Retrying without waiting puts more load on a
   server that is already struggling.
3. **Leaving on success:** `break`.

## Exponential backoff

Instead of waiting the **same** time on every attempt, doubling the wait is a
better habit: 1 second, 2 seconds, 4 seconds... If the server has a short
hiccup you recover quickly; if the problem is long you do not tire it for
nothing. This is called **exponential backoff**.

```python
def get_with_retry(url, attempts=4):
    delay = 1
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                return r                 # success, or a 4xx to fix
        except (requests.Timeout, requests.ConnectionError):
            pass                         # temporary: try again
        if attempt < attempts - 1:
            time.sleep(delay)
            delay *= 2                   # 1, 2, 4, ...
    return None                          # every attempt used up
```

The function returns a `4xx` at once: waiting does not fix that error. On
`5xx` and connection problems it waits and tries again; it does not wait after
the last attempt. If none of them works it returns `None` and the decision is
left to the caller.

Real systems also add a little randomness to the wait (jitter), so that a
thousand clients that failed at the same moment do not all come back in the
same second and swamp the server again.

## Knowing when to give up

`/broken` always returns `500`; it will not get better however often you try.
A retry is a **plan**, not a **hope**: try a set number of times, then give
up and report the situation clearly.

```python
r = get_with_retry(BASE + "/broken", attempts=3)
if r is None or r.status_code >= 500:
    print("the service is down; try again later")
```

A good program says what happened when it gives up: which address, how many
attempts, the last error. "Something went wrong" is not enough.

## Summary

- Errors come in two kinds: a **bad response** (4xx/5xx, look at the code)
  and **no response** (an exception: `Timeout`, `ConnectionError`).
- **Give every request a `timeout=`**; by default requests waits for ever.
- They all belong to the `requests.RequestException` family; catch from
  specific to general.
- Retry only temporary errors (`Timeout`, `ConnectionError`, `5xx`, `429`)
  and only idempotent requests; fix `4xx`.
- A retry needs an upper limit and a wait; **exponential backoff** (1, 2, 4
  s) is a good default.
- When the attempts run out, give up and report the situation clearly.
