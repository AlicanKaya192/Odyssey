| Step | What it does | Section | Its measure |
|---|---|---|---|
| Mask | Hides personal data before the question goes to the search and the log | 14 | Caught / missed on example sentences |
| Search | Finds the most relevant article, then its sentences | 09 | key@k, recall@k, MRR |
| Fit to the budget | Keeps the sources within the token limit | 07 | Tokens per question, cost |
| Build the prompt | Numbered sources + rules + question | 10 | — |
| Get the answer | The model (here the example reader) | 06, 10 | Correct, wrong, missed |
| Verify | The source number and the numbers | 08 | Inventions caught |
| Log | The masked question, result, tokens, cost | 07 | Usage summary |
| Measure | Compare on the evaluation set | 11 | Groups, interval |

**Keep in mind:**

- In the section two-stage search brought the wrong answers from 2 to 0; misses
  rose from 7 to 9, tokens from 132 to 154.
- Verification caught "5 years", which is not in the source.
- Every step has its own measure; the system is improved with them.
