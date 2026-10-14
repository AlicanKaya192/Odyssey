| Term | Meaning |
|---|---|
| **Structured output** | Asking for the answer in a form with set fields, such as JSON |
| **Schema** | The definition of which fields come, with which types and values |
| **Parsing** | Turning text into JSON, cleaning harmless additions (a code block, a sentence in front) |
| **Validation** | Checking the parsed data against the schema: fields, types, allowed values, patterns |
| **Repair loop** | Sending an invalid answer back to the model with an error message and asking again |
| **Limit of tries** | How many times at most the repair loop goes round |

**Keep in mind:**

- In the lesson four of six example replies were parsed, and only three
  followed the schema.
- A single-quoted object is not JSON; the cause of cut-off JSON is
  `max_tokens` (`finish_reason` is `length`).
- An API setting that enforces the schema only guarantees the form; the
  program checks that the value was chosen correctly.
- In the repair the second call's input went from 16 to 114 tokens; error
  messages should be readable sentences.
