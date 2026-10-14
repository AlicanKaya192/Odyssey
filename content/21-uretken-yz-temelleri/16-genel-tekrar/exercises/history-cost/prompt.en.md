`history_cost(tokens, price_in, price_out)` should take the token counts of
the user messages arriving in order in a conversation. In every call all the
messages so far are sent as input (the answers are ignored) and every answer is
20 tokens. Return `[total input tokens, total cost]`; prices per million
tokens, the cost a `float` rounded to 6 places (07).

**Expected output:**

```
[94, 0.000167]
```
