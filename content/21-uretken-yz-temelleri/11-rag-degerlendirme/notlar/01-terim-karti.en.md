| Term | Meaning |
|---|---|
| **Evaluation set** | Hand-labelled questions: the right document and the answer phrase |
| **recall@k** | The share of questions whose answer phrase is in the first k chunks |
| **MRR** (mean reciprocal rank) | The average of one over the rank of the right chunk |
| **Retrieval error** | The right chunk never got into the prompt |
| **Reading error** | The right chunk was in the prompt but the answer is wrong or missing |
| **Abstention precision** | The share of "not found" answers that go to questions with no answer |
| **Abstention recall** | The share of questions with no answer recognised with "not found" |
| **Resampling** (bootstrap) | Drawing the questions with replacement and computing the measure again and again |
| **Evaluation with a model** | Having another model score the answer; that model has its own errors too |

**Keep in mind:**

- In the section recall@1 was 0.71, recall@10 0.96; 7 of the 9 missed answers
  were retrieval errors. The search comes first.
- At threshold 3 recall was 1.00 but precision 0.12: the two measures are read
  together.
- On 24 questions the 90% interval of a two-question difference was 0–4; it is
  not safe to decide on a small set.
