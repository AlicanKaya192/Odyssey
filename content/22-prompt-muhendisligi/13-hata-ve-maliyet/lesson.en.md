# Errors, Retries and Cost

So far every call returned an answer. A real service is not like that: the
request limit fills up, the service cannot answer for a moment, a request
does not fit in the context window, an answer is cut halfway. A large part
of an LLM application's code deals with these cases. In this section we
measure which error is retried, how long to wait, what a cut answer costs
and a simple cache that lowers the cost.

The errors in this section also come from the script of the recorded-reply
client: if an error object is put into the script, that error is raised
for that call. The error names and messages are **examples**; the error
types and codes of real services differ from one another.

## Which error is retried?

Errors need to be split into two groups:

- **Temporary errors:** the request limit is full (HTTP 429 in most
  services), the service could not answer for a moment (5xx). The same
  request may succeed a little later; retrying makes sense.
- **Permanent errors:** the request does not fit in the context window,
  the message list is broken, the credentials are wrong. However often you
  send the same request you get the same error; retrying only wastes time.
  The request has to change.

When retrying, doubling the waiting time each time is a common way:
**exponential backoff**. In the code we wait with a function passed in
from outside instead of `time.sleep`; so in the example we can see which
times were waited without really waiting:

```python
import time

from llm_client import ChatClient, ContextLengthError, RateLimitError, ServerError

RETRYABLE = (RateLimitError, ServerError)


def call_with_retry(client, messages, attempts=4, base=1.0, sleep=time.sleep):
    for attempt in range(attempts):
        try:
            return client.chat(messages, max_tokens=60)
        except RETRYABLE:
            if attempt == attempts - 1:
                raise
            sleep(base * 2 ** attempt)


MESSAGES = [{"role": "user", "content": "Where is my order ORD-48213?"}]
CASES = {
    "two failures": [RateLimitError("429 too many requests"),
                     ServerError("503 unavailable"),
                     "Your parcel left the depot today."],
    "always busy": [RateLimitError("429 too many requests")] * 4,
}
for name, script in CASES.items():
    waits = []
    try:
        reply = call_with_retry(ChatClient(script), MESSAGES, sleep=waits.append)
        result = reply.text
    except RateLimitError as error:
        result = f"gave up ({error})"
    print(f"{name}: waits {waits} -> {result}")

LONG = [{"role": "user", "content": "Where is my order? " * 8}]
waits = []
try:
    call_with_retry(ChatClient(["never sent"], context_window=60), LONG,
                    sleep=waits.append)
except ContextLengthError as error:
    print(f"too long: waits {waits} -> {error}")
```

```text
two failures: waits [1.0, 2.0] -> Your parcel left the depot today.
always busy: waits [1.0, 2.0, 4.0] -> gave up (429 too many requests)
too long: waits [] -> 62 input + 60 output tokens > window of 60
```

In the first scenario the third attempt got an answer after two temporary
errors, with waits of 1 and 2 seconds in between. In the second scenario
the service is always busy: after waiting 1, 2 and 4 seconds, an error
came on the fourth attempt too, so the function gave up and passed the
error up. The number of attempts must have a limit; otherwise the
application waits forever. In the third case the request does not fit in
the window; this error is not in `RETRYABLE`, so it went up at once
without any waiting. To solve it the request has to be shortened (trimming
the history, splitting the document).

Some services also say in a 429 answer how long to wait (the
`Retry-After` header). If they do, follow that time instead of your own
calculation.

## If everyone retries at once: random waiting

When the service stops for a moment, all the clients using it get an error
at the same time. If all of them say "wait 1 second" by the same rule, a
second later all of them come back at once and the service fills up
again. The remedy is to add randomness to the waiting: **jitter**. Below,
100 clients get an error at the same moment; the service accepts at most
20 requests every 0.1 seconds:

```python
import random

CLIENTS, CAPACITY, SLOT = 100, 20, 0.1


def retry_times(rng, jitter, base=1.0):
    if jitter:
        return [rng.uniform(0, base) for _ in range(CLIENTS)]
    return [base] * CLIENTS


def rejected(times):
    slots = {}
    for t in times:
        slots[int(t / SLOT)] = slots.get(int(t / SLOT), 0) + 1
    return max(slots.values()), sum(max(0, n - CAPACITY) for n in slots.values())


rng = random.Random(1)
for jitter in (False, True):
    busiest, failed = rejected(retry_times(rng, jitter))
    label = "with jitter" if jitter else "no jitter"
    print(f"{label}: busiest {SLOT} s {busiest} requests, rejected again {failed}")
```

```text
no jitter: busiest 0.1 s 100 requests, rejected again 80
with jitter: busiest 0.1 s 16 requests, rejected again 0
```

Without jitter all 100 clients fell into the same 0.1 seconds and 80 were
rejected again. When the wait is chosen at random between 0 and 1 second,
the busiest slot had 16 requests and with this seed none was rejected. In
retry code the wait `base * 2 ** attempt` becomes
`random.uniform(0, base * 2 ** attempt)`.

## The danger of retrying: a job done twice

Repeating "answer this question" to the model is harmless. But if a tool
call **changes** something (cancelling an order, starting a refund),
retrying it may do the job twice. A timeout is even sneakier: since no
answer came, the request is thought not to have been processed, yet it
may have been processed and its answer lost on the way.

The solution is to put a **request id** (idempotency key) on every request
that changes something: a second request with the same id is not
processed again, it returns the first result. In short, retrying happens
automatically only for jobs that are safe to repeat.

## A cut answer is paid twice

If the answer hits the `max_tokens` limit it is cut halfway and
`finish_reason` becomes `"length"`. A program that expects JSON cannot
parse cut JSON. A common remedy is to raise the limit and ask again. But
with every new request the prompt is sent from the start:

```python
import json

from llm_client import ChatClient

REPLY = ('{"category": "returns", "order": "ORD-10077", '
         '"summary": "The customer wants to return the tent."}')
SYSTEM = "Answer with JSON: category, order, summary."
MESSAGES = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Can I return the tent from ORD-10077?"}]


def ask_json(client, max_tokens, tries=3):
    paid_in = paid_out = 0
    for _ in range(tries):
        reply = client.chat(MESSAGES, max_tokens=max_tokens)
        paid_in += reply.input_tokens
        paid_out += reply.output_tokens
        if reply.finish_reason != "length":
            return json.loads(reply.text), paid_in, paid_out
        print(f"  cut at {max_tokens}: ...{reply.text[-20:]}")
        max_tokens *= 2
    raise ValueError("the answer did not fit")


for start in (12, 48):
    print(f"max_tokens {start}:")
    data, paid_in, paid_out = ask_json(ChatClient([REPLY] * 3), start)
    print(f"  {data['category']}, paid {paid_in} in + {paid_out} out")
```

```text
max_tokens 12:
  cut at 12: ...egory": "returns", "
  cut at 24: ...der": "ORD-10077", "
  returns, paid 108 in + 78 out
max_tokens 48:
  returns, paid 36 in + 42 out
```

The request that started at 12 tokens was cut twice: first at 12, then at
24 tokens. The third call fitted with 48 tokens. In total 108 input and 78
output tokens were paid; the prompt was sent three times and the tokens of
the two cut answers were generated too (the fee is usually for generated
tokens). The request that started at 48 finished in one call with 36
input + 42 output tokens. `max_tokens` is chosen for the expected length
of the answer: if it is too small the answer is cut and asked for again,
while a large limit brings no fee, it only reserves room in the window.
The number of attempts is limited here too; if the answer never fits, the
function raises an error.

## Cost: a cache

We saw how cost is calculated in the Generative AI Fundamentals module:
input tokens × input price + output tokens × output price. The ways of
lowering the cost in an application mostly came up in earlier sections: a
short system message, as many examples as needed, a trimmed history, as
much `max_tokens` as needed. There is one more way: **not sending the same
request twice.**

Suppose the support page has five ready question buttons. Of 100 requests,
60 come from these buttons and 40 from messages customers wrote
themselves (the 40 messages in `shop_data`). This traffic was made up for
the lesson; it is not a measurement of a real shop:

```python
import random

from llm_client import count_message_tokens
from shop_data import TICKETS

SYSTEM = ("You are the support assistant of an outdoor shop. Answer in at most "
          "three sentences. Never promise a refund, a delivery date or a discount.")
BUTTONS = ["How do I return an item?", "How long does a refund take?",
           "What does the warranty cover?", "Which payment methods do you accept?",
           "How much is shipping?"]
rng = random.Random(3)
traffic = [rng.choice(BUTTONS) for _ in range(60)] + [t["text"] for t in TICKETS]
rng.shuffle(traffic)


def messages_for(text):
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": text}]


cache, calls, sent, saved = {}, 0, 0, 0
for text in traffic:
    tokens = count_message_tokens(messages_for(text))
    key = (SYSTEM, text, 0.0)
    if key in cache:
        saved += tokens
        continue
    cache[key] = f"answer {len(cache)}"
    calls += 1
    sent += tokens
hits = len(traffic) - calls
print(f"{len(traffic)} requests, {calls} model calls, {hits} from cache")
print(f"input tokens sent {sent}, saved {saved}")
```

```text
100 requests, 45 model calls, 55 from cache
input tokens sent 2888, saved 3313
```

55 of the 100 requests were answered from the cache and only 45 calls
went to the model: each of the five button questions once, each of the
customers' 40 messages once. 3313 input tokens were never sent; more than
the 2888 that were. For a cache to help, the same request has to really
repeat: the messages customers wrote themselves never repeated in this
traffic. The key contains everything that affects the answer: the system
message, the user's text and the setting (temperature). When the system
message changes, the old answers become invalid by themselves. A request
whose answer depends on the customer's data (the status of their order)
must not be given to someone else from the cache; its key belongs to that
customer and is not shared. Some services also offer their own prefix
cache for requests that start the same way; the conditions differ from
service to service.

## What happens when we give up?

Retries can run out too. Then the program should not crash but show the
user an honest message: "We cannot answer right now, your message has been
passed to an agent." For that:

- Put a **time limit** on the total waiting. A user does not wait 30
  seconds; if the next wait would cross the limit, give up without
  waiting.
- When giving up, give a **fallback answer** and log the request, so a
  person can look at it later.
- Count the errors. If the rate of temporary errors suddenly rises, the
  problem may be in the service rather than your code; if permanent errors
  rise, the problem is most likely in your requests.

## Summary

- Temporary errors (request limit, service error) are retried; permanent
  errors (not fitting the window, a broken request) are not, the request
  is changed.
- The wait grows exponentially and there is a limit on attempts. If the
  service says how long to wait, that is followed.
- Random waiting (jitter) stops clients that got an error at the same time
  from all coming back together.
- A request that changes something is not retried automatically, or it
  carries a request id; otherwise the job may be done twice.
- Asking again for a cut answer with a larger limit makes you pay for the
  prompt again; `max_tokens` is chosen for the expected answer.
- A cache does not send the same request a second time; the key must
  contain everything that affects the answer.
- When giving up the program does not crash: a time limit, a fallback
  answer and a log.
