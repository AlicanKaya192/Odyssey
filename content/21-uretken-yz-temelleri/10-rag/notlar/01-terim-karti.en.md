| Term | Meaning |
|---|---|
| **RAG** (retrieval-augmented generation) | Finding relevant chunks, giving them to the model and basing the answer on them |
| **Retrieval** | The step of finding the chunks most relevant to the question |
| **Context** | The numbered chunks put into the prompt |
| **Citation** | Writing which chunk the answer comes from, with its number |
| **Abstain threshold** | The least support needed to answer; low means more wrong answers, high more misses |
| **Wrong retrieval** | The search not finding the right chunk |
| **Misusing what was retrieved** | The answer resting on the wrong chunk or a wrong reading while the right chunk is there |

**Keep in mind:**

- The setup without sources missed all 24 questions; with sources, threshold 2
  gave 15 correct, 2 wrong, 7 missed; threshold 1 gave 17 correct, 7 wrong.
- The sources added 58 tokens to every call on average.
- The section's reader is a crude example standing in for a real model; the
  numbers show how the setup behaves.
