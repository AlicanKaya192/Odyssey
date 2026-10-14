The flow of a program that uses a structured answer:

| Step | What is done? | If it fails |
|---|---|---|
| 1 | Look at `finish_reason` | `length`: raise `max_tokens` or ask for a shorter schema |
| 2 | Try the text as it is with `json.loads` | Go to step 3 |
| 3 | Remove the code block marks, try again | Go to step 4 |
| 4 | Try the part between the first `{` and the last `}` | Invalid JSON: repair loop |
| 5 | Validate against the schema | Repair loop with the error list |
| 6 | If the limit of tries is reached | Send to a person or the `needs_review` path |

**When writing the schema:**

- Write every field's name, type and allowed values clearly in the
  instruction; if possible show an example JSON.
- State the empty-value rule, such as "`null` if unknown"; otherwise the
  model may make up a value.
- Keep the number of fields to what is needed; every field adds tokens
  and a chance of error.

**Error messages:**

- Short, readable sentences that say the fix: "urgent must be true or
  false".
- List the allowed values in the message; the model sees what to choose.
- No personal data or internal rules; the message goes to the model.

**Common mistakes:**

- **Fixing an answer that is not JSON with a guess.** It becomes unclear
  which forms are accepted.
- **Taking parsed JSON for correct.** In the lesson a valid JSON had
  three schema errors.
- **Repairing without limit.** Every try sends more tokens; set a limit.
