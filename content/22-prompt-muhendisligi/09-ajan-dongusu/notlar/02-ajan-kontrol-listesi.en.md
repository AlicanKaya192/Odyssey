Before running an agent:

| Question | What happens without an answer? |
|---|---|
| Does the order of the steps really change with the input? | An agent is built where a chain would do; more expensive and harder to test |
| What is the step limit? | A stuck agent goes round forever |
| What is the token budget? | A long history is paid again every round |
| Which tools are on the allow-list? | The model may call an unwanted job |
| Are irreversible jobs confirmed? | The agent does a cancellation or a payment on its own |
| Where does the job go when a limit is reached? | The customer is left without an answer |

**In the loop, every round:**

1. Call the model; write the input tokens into the trace.
2. If there is no tool call, take the answer and validate it (length,
   promises, grounding).
3. For every tool call: is it a repeat? is it on the allow-list? are the
   arguments right? does it need confirmation?
4. Add the result or the error to the history as a `tool` message.
5. Check the step limit and the token budget.

**Common mistakes:**

- **Leaving the stopping to the model.** The model may not say "done";
  the program stops it.
- **Running the same call again and again.** Both the tool and tokens are
  wasted.
- **Counting a clean end of the loop as success.** The answer may be
  half; measure with an evaluation set.
- **Keeping no trace.** You cannot find in which round a wrong answer
  started.
