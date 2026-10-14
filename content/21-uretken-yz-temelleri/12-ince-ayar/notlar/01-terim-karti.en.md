| Term | Meaning |
|---|---|
| **Pre-training** | The first training on a very large amount of data on a general task (the next token) |
| **Fine-tuning** | Continuing to train a pre-trained model with new data |
| **Freezing** | Not updating a layer's weights during fine-tuning |
| **Catastrophic forgetting** | The old task breaking after fine-tuning on new data |
| **Replay** | Mixing examples of the old task into the fine-tuning data |
| **Instruction tuning** | Fine-tuning with (instruction, good answer) pairs |
| **Preference alignment** | Learning from pairwise preferences and steering the model to preferred answers |
| **Reward model** | A model that gives an answer a preference score |
| **Bradley–Terry** | The probability that a is preferred to b is σ(r(a) − r(b)) |
| **Best-of-n** | Choosing the answer with the highest reward from n answers |
| **Reward hacking** | What the reward measures rising while what is wanted does not |

**Keep in mind:**

- In the section fine-tuning on new data alone dropped the old task to 6.5%;
  mixing in 50 old examples kept it at 94.5–98%.
- The reward model learnt values close to the hidden weights from the
  preferences alone; choosing from 8 answers with the reward raised correct
  answers from 50% to 99%.
- The reward learnt from biased labellers chose long answers; correctness
  stayed at 78%.
