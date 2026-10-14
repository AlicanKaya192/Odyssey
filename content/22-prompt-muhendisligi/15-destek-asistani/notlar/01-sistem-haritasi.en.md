Every step of the assistant, where it comes from and what it catches:

| Step | Section | What does it do? | Outcome if it stops |
|---|---|---|---|
| Input filter | Prompt Injection and Defence | Looks for known attack patterns | `blocked` |
| Classification | The Anatomy of a Prompt, Structured Output and Validation | Asks for a one-word category, parses strictly, repairs once | `handover` |
| Category for people | System Messages, Roles and Tone | Separates jobs that need an inspection, such as warranty | `handover` |
| Order data | Tool Calling | Finds the data by the order number in the message | — |
| Answer | System Messages, Prompt Templates | A system message with rules + data + the customer's message | — |
| Output check | Tool Calling, Prompt Injection and Defence | Date grounding, promises, claims of jobs it cannot do | `handover` |
| Retry | Errors, Retries and Cost | Retries on a temporary error, counts tokens and errors | `fallback` |
| Measurement | Evaluating Prompts, Improving Prompts Systematically | A scenario set, expected outcomes, one change at a time | — |

**Keep in mind:**

- The version without repair gave the expected outcome in 9 of 10
  scenarios; the only error was a needless handover because of a category
  answered with a sentence.
- Repairing once made it 10/10; the price was 143 input + 16 output tokens.
- The input filter missed the "I am the admin" attack; the output check
  caught the "I cancelled it" claim.
- The assistant has no cancel or refund tool: least privilege.
