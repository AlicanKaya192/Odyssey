The cases met in an LLM call and what to do:

| Case | Retry? | What is done? |
|---|---|---|
| Request limit (429) | Yes | Exponential wait + jitter; if the service says a time, follow it |
| Service error (5xx) | Yes | Exponential wait + jitter, a limit on attempts |
| Timeout | Carefully | Yes for a reading request; for a changing request only with an idempotency key |
| Not fitting the window | No | Trim the history, split the document, lower `max_tokens` |
| Broken request (role, content) | No | Fix the code; this is a program bug |
| Wrong credentials | No | Fix the setting; sending again changes nothing |
| `finish_reason == "length"` | Once, with a larger limit | Choose `max_tokens` for the expected answer; the prompt is paid again |
| All attempts used up | — | Fallback answer + log; the program does not crash |

**A retry skeleton:**

```python
for attempt in range(attempts):
    try:
        return client.chat(messages, max_tokens=max_tokens)
    except (RateLimitError, ServerError):
        wait = random.uniform(0, base * 2 ** attempt)
        if attempt == attempts - 1 or waited + wait > deadline:
            return FALLBACK
        sleep(wait)
        waited += wait
```

**Common mistakes:**

- **Retrying every error.** A permanent error comes the same with every
  attempt; it only keeps the user waiting.
- **Unlimited attempts.** If the service is down for long, the program
  never answers.
- **A fixed wait.** Clients that failed together come back together.
- **Retrying a changing request without an id.** The job may be done
  twice.
- **Leaving something that affects the answer out of the cache key.** When
  the system message or a setting changes, the old answer keeps coming
  back.
