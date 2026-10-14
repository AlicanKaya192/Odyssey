An instruction that asks for a stepwise answer and the program that uses
it are built like this.

**Instruction:**

```text
Work out the answer step by step, one operation per line,
in the form "a + b = c". The last line must be
"Answer: <number>" with no other text.
```

**Program:**

| Step | What is done? | If it fails |
|---|---|---|
| 1 | Parse the last line (`^Answer:\s*number$`) | Ask again or send to a person |
| 2 | Compute the operations in the steps again | Calculation error: do not use the answer |
| 3 | If the result can be computed with code, compare | Reasoning error: use the code's result |
| 4 | Show the customer only the final answer | — |

**When is it not used?**

- In one-step jobs (picking a category, extracting a short fact).
- If the result can be computed exactly with code: then ask the model only
  for the numbers and let the code calculate.
- If the token budget is tight and an error costs little.

**Common mistakes:**

- **Taking the final answer from anywhere in the text.** One of the
  intermediate results in the steps may be taken for the answer.
- **Trusting the answer because the steps look right.** In the lesson a
  correctly computed but incomplete step gave a wrong amount.
- **Taking the majority for correctness.** With a model that repeats the
  same error, the majority is wrong too.
- **Showing the steps to the customer.** Wrong intermediate results and
  internal rules become visible.
