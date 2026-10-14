A skeleton of a system message for a support assistant:

```text
You are the support assistant of <shop>.
Be friendly and brief: at most 3 sentences.
Answer in the language of the customer.
Rules:
1. Talk only about orders, shipping, returns and products.
2. Never promise a refund or a discount.
3. If you do not know, say so and offer to ask a colleague.
```

**Two questions for every rule:**

| Rule | Told to the model? | Checked with code? |
|---|---|---|
| At most 3 sentences | Yes | Yes: number of sentences |
| No promises | Yes | Yes: promise patterns |
| Only shop topics | Yes | Partly: needs a topic classifier |
| Say so if unsure | Yes | No: measured with an evaluation set |

**What happens to an answer that fails?**

| Problem | What to do |
|---|---|
| A promise, a discount, personal data | Do not send; pass it to a person |
| Too long | Ask again once, asking it to shorten |
| A needless sentence such as "As an AI ..." | Ask again or drop the sentence |

**Common mistakes:**

- **Writing a rule only in the system message and not checking it.** When
  a user writes "forget your rules", the answer check is the last
  defence.
- **Putting secret information in the system message.** Users can pull
  it out.
- **Not logging the version.** After a complaint you cannot find which
  rules were in force.
- **Padding the role with a long made-up background.** The tokens are
  paid in every call.
