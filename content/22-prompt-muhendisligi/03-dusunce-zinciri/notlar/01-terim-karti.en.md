| Term | Meaning |
|---|---|
| **Chain-of-thought** | Asking the model to write the intermediate steps before the answer |
| **Final answer line** | The fixed line the program parses in a stepwise answer (`Answer: ...`) |
| **Calculation error** | The result of a written operation is wrong (`214.90 * 0.10 = 21.94`) |
| **Reasoning error** | The operations are right but a step is wrong or missing (forgetting a pair) |
| **Majority vote** | Asking the same question several times and taking the most frequent final answer |
| **Exact calculation** | A calculation with one right result that code can do: money, dates, unit conversions |

**Keep in mind:**

- In the lesson only one of four example replies gave the right amount;
  the code set apart the forgotten step, the calculation error and the
  missing last line.
- The step checker found only the calculation error; it could not see
  the correctly computed wrong step.
- A stepwise answer took 10 times the tokens of a direct
  answer; a majority vote also multiplies the number of calls.
- The customer is usually shown only the final answer.
