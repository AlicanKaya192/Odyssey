| Technique | When? | Watch out |
|---|---|---|
| Strict parser | If the answer goes into a program | Do not search for the category inside the text; an unclear answer is `needs_review` |
| Clear instruction + delimiter | In every prompt | Write measurable rules; separate data with a delimiter and escape it |
| Few-shot prompt | If a format or a boundary is better shown by example | Examples should cover the categories; every example costs tokens |
| Step-by-step reasoning | For reasoning in many steps | Let code do the calculation; the answer with steps is much longer |
| Structured output | If the answer is used as data | Parse, validate with a schema, repair once |
| System message | If a role, tone and rules are needed on every call | Build it from settings, keep the version digest; write nothing secret |
| Template | The same prompt with different data | A missing value should raise an error; cut long text in the middle |
| Chain | If a job splits into small, checkable steps | A failed step should stop the chain |
| Tool calling | If the model needs current data or an action | Validate the call; confirmation for irreversible jobs; ground the answer in the result |
| Agent loop | If the number of steps is not known in advance | A limit on rounds and tokens; catch a repeated call |
| Memory | When the conversation grows | Last messages + important facts kept separately; a summary may drop facts |
| Evaluation | With every change | Form and correctness separately; a bootstrap interval for a small difference |
| Injection defence | When outside text is read, if there are tools | Layered: detector, least privilege, confirmation, output check |
| Retry | On temporary errors | Exponential wait + jitter, limits on attempts and time, a fallback answer |
| Cache | If the same request repeats | The key contains everything that affects the answer; do not share personal data |
| Systematic improvement | While developing the prompt | Decide on the development set, look at the test once at the end |

**The module's numbers (all with recorded replies or the toy model):**

- The system message is 73–78% of the tokens for short messages; 67% for
  40 messages in the capstone.
- Pattern detector: precision 0.8, recall 0.57.
- Memorisation: 1.00 on development, 0.75 on test.
- The assistant: 9/10 without repair, 10/10 with repair.
