There are two common forms for putting examples into a prompt.

**1. Message pairs.** Each example is a `user` message and its
`assistant` answer; the new input comes last:

```text
system:    Put the message into one category: shipping, returns, ...
user:      My parcel should have arrived on Monday.
assistant: shipping
user:      Can I return boots I only tried on at home?
assistant: returns
user:      <new message>
```

**2. A single text.** The examples sit inside the same instruction text,
in a fixed pattern:

```text
Put the message into one category: shipping, returns, ...

Message: My parcel should have arrived on Monday.
Category: shipping

Message: Can I return boots I only tried on at home?
Category: returns

Message: <new message>
Category:
```

| | Message pairs | A single text |
|---|---|---|
| Showing the form | The answer is the whole message | The answer follows the `Category:` line |
| Parsing | The answer is the label itself | If extra lines come, take the first one |
| When? | Chat models | Models or templates that expect one text |

**Order of choices:**

1. Split the pool and the test set; no test message becomes an example.
2. Take at least one example from each category (balanced) and give them
   in a shuffled order.
3. Prefer hard examples (those between two categories).
4. Before adding examples, measure the token price; measure with an
   evaluation set whether the increase is worth it.

**Common mistakes:**

- **Giving the examples sorted by category.** The last example always has
  the same category.
- **Different forms in the example answers.** If one is "shipping" and
  another "Shipping.", the model may produce both.
- **Using a test message as an example.** The measured success becomes
  memorisation.
