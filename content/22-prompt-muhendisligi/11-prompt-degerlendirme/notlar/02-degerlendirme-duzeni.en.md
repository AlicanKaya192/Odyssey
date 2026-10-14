A setup for evaluating a prompt change:

| Step | What is done? |
|---|---|
| 1 | Fix the evaluation set (inputs + right answers) |
| 2 | Run the old and the new version on the same set with the same settings (temperature, `max_tokens`) |
| 3 | Record the answers: version name, input, answer, tokens |
| 4 | Score form, validity and correctness separately |
| 5 | Split the errors into kinds (confused pairs, unparsable ones) |
| 6 | Look at the inputs where the versions give different results; find the range of the difference with resampling |
| 7 | Decide on the test set; the score on the development set is optimistic |

**A rubric for open-ended answers (example):**

| Question | Score |
|---|---|
| Does it answer the question? | 0 / 1 |
| Does it give the product name correctly? | 0 / 1 |
| Does it contain a promise or something banned? | 0 / 1 (0 if it does) |
| At most 3 sentences? | 0 / 1 (with code) |

Questions code can check are scored with code; for the rest, if a scoring
model is used, its agreement with human scores is first measured on 30–50
answers.

**Common mistakes:**

- **Looking at a single total score.** A format error and a wrong category
  need different fixes.
- **Trusting a small difference on a small set.** On forty messages even a
  five-message difference was not certain.
- **Improving and deciding on the same set.** The score becomes
  optimistic.
- **Using a scoring model without checking it.** It may favour long
  answers.
