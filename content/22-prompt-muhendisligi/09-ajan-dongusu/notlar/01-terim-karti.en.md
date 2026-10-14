| Term | Meaning |
|---|---|
| **Agent** | A loop in which the model picks the next action every round and the program runs the tools |
| **Round** (step) | One model call and the tools run after it |
| **Step limit** | How many rounds at most the loop goes |
| **Token budget** | The most tokens one agent run may spend |
| **Trace** | Each round's tool, argument, result and tokens |
| **Catching repetition** | Not running the same call with the same arguments a second time |

**Keep in mind:**

- In the lesson the agent that solved the question spent 246 input tokens
  in three rounds, the repeating agent 516 in five; the step limit stopped
  the repeating agent.
- The agent that recovered after an error switched to the right tool but
  answered only half the question: a loop ending cleanly does not mean
  the answer is complete.
- Every round sends the history again; a round's input tokens grow every
  round.
- If the steps are fixed, a chain is more predictable and cheaper.
