| Term | Meaning |
|---|---|
| **Temporary error** | An error where the same request may succeed a little later: the request limit (429), a service error (5xx) |
| **Permanent error** | An error that sending again does not fix: not fitting the window, a broken request, wrong credentials |
| **Exponential backoff** | Doubling the waiting time with every attempt: 1, 2, 4 seconds |
| **Jitter** | Adding randomness to the wait, so clients that failed together do not come back together |
| **Idempotency key** | An id put on a request that changes something; a second request with the same id is not processed again |
| **Cut answer** | An answer that hits `max_tokens`; `finish_reason` is `"length"` |
| **Cache** | Keeping the answer of a request so it is not sent to the model a second time |
| **Fallback** | The honest message shown to the user when the attempts run out |

**Keep in mind:**

- In the lesson the third attempt got an answer after two temporary errors
  (waits of 1 and 2 seconds); the request that did not fit the window
  failed without any waiting.
- When 100 clients retried at once, 80 were rejected again without jitter;
  with jitter the busiest slot had 16 requests.
- The JSON request that started at 12 tokens was cut twice; three calls
  paid 108 input + 78 output tokens, against 36 + 42 when starting at 48.
- The cache did not send 55 of 100 requests to the model.
