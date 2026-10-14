`chat_cost(price_in, price_out)` should ask the starter code's three
questions with `ChatClient(REPLIES)`, sending the **whole history** in every
call (no system message; add each answer to the history as an `assistant`
message, `max_tokens=50`). Return the totals of the replies' `input_tokens`
and `output_tokens` and the cost with prices given per million tokens:
`[input total, output total, cost]`; the cost a `float` rounded to 8
places.

**Expected output:**

```
[97, 17, 7.4e-05]
[97, 17, 0.00033]
```
