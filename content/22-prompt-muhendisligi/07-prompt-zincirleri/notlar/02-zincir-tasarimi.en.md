When building a chain, fill this table for every step:

| Step | Input | Output | Validation | If it fails |
|---|---|---|---|---|
| Classify | The customer's message | `{"category": ...}` | Is the category in the list? | Ask again, then a person |
| Extract | The customer's message | `{"order_id": ...}` | Is the field there, does it match the pattern? | Treat as `null` or ask again |
| Write the answer | Message + relevant rule | Plain text | Answer rules (length, no promises) | Shorten or a person |

**Design questions:**

1. Does this job really consist of different sub-jobs?
2. Does an error in one step spoil the following ones? If so, check that
   step separately.
3. Which context does each step need? Do not send what is not needed.
4. Which steps are not needed for every message? Skip them with a
   condition.
5. Are the chain's total tokens and calls more than a single prompt's?
   Measure.

**Log:**

- For each step: name, success, input and output tokens, time.
- If the chain stopped: the step where it stopped and why.
- The names and versions of the templates used.

**Common mistakes:**

- **Giving a step's output to the next without validating it.** The error
  grows along the chain.
- **Splitting a simple job into a chain.** Only calls and waiting grow.
- **Sending all the context to every step.** The chain's benefit of
  choosing context is lost.
- **Not logging why it stopped.** It is unknown which step to improve.
