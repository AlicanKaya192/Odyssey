| Term | Meaning |
|---|---|
| **Evaluation set** | Inputs with known right answers; every prompt version is scored on the same set |
| **Exact** | The answer equals the right label without any cleaning |
| **Valid** | The answer is in a form the program can parse |
| **Right** | The parsed value is the right label |
| **Confused pair** | The two categories most often mixed up with each other |
| **Model as a judge** | A separate model call that scores open-ended answers with a rubric |
| **Regression** | A fix in one place breaking another |

**Keep in mind:**

- In the lesson the answers of `v1` and `v2` were example replies written
  for the lesson; the numbers show the scoring method, not a measurement
  of a model.
- `v1`: exact 26, valid 36, right 31; `v2`: 35, 39, 36 (out of 40
  messages).
- In both versions the most confused pair is refunds ↔ payment.
- The difference is 0.125 but the resampling 90% interval is between 0 and
  0.25: on forty messages even a five-message difference is not certain.
