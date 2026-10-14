| Term | Meaning |
|---|---|
| **Prompt chaining** | Splitting a job into steps done by separate calls; one step's output is the next one's input |
| **Step validation** | Checking each step's output before giving it to the next step |
| **Stopping the chain** | Not going on at a step that cannot be validated and logging where it stopped |
| **Step log** | Each step's name, result and tokens |
| **Conditional step** | A step skipped or chosen according to the earlier step's output |
| **Choosing context** | Sending each step only the information it needs (such as a single rule) |

**Keep in mind:**

- In the lesson the first step gave no JSON for the second message; the
  chain stopped at classification and the log showed where.
- In this example the single prompt took 412 tokens because it carried
  all the rules, and the chain's three calls 215 tokens in total; with
  short rules the result could turn the other way.
- Skipping the extraction step for categories that do not need it took
  the number of calls on 10 test messages from 30 to 26.
- The decision to skip depends on the earlier step being right.
