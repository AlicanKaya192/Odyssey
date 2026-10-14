| Term | Meaning |
|---|---|
| **Tool** | A function the program offers the model: fetching an order, computing an amount |
| **Tool schema** | The part that goes to the model: the tool's name, description, arguments |
| **Tool call** | The request the model returns instead of an answer: which tool, which arguments |
| **Tool result** | The result the program gives the model in a `tool` message after running the tool |
| **Allow-list** | The list of tools the program agrees to run |
| **Confirmation** | The customer's or an employee's approval before an irreversible job is run |
| **Grounding check** | Checking whether the facts in the final answer are the same as the tool result |

**Keep in mind:**

- The model does not run the tool; the program validates and runs the
  call.
- In the lesson one of five example calls returned order information; two
  gave error results, the unknown tool was rejected and the cancellation
  waited for confirmation.
- A question that used a tool took two calls; the second call carries the
  question, the tool call and its result together.
- An answer writing a date that was not in the tool result was caught by
  the grounding check.
