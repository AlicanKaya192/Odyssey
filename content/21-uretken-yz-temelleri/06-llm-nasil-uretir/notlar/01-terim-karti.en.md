| Term | Meaning |
|---|---|
| **Large language model** (LLM) | A model trained on a very large amount of text that predicts the next token |
| **Token** | The unit the model processes: a word, a piece of a word or a symbol |
| **Chat template** | The format that turns the message list into a single sequence with role markers |
| **Role** | The owner of a message: `system` (general instructions), `user`, `assistant` |
| **Stop marker** | The model's special token showing that the answer is finished |
| **`max_tokens`** | The upper limit on the number of tokens to generate |
| **Finish reason** | `stop`: the answer is complete; `length`: it was cut at the limit |
| **Temperature** | The randomness of sampling; 0 = the most likely token at every step |
| **Hallucination** | Producing fluent but wrong text for a question with no basis |
| **Stateless API** | The model does not remember earlier calls; the history is sent in every call |

**Keep in mind:**

- The model does not answer the question, it continues the text; the template
  says where the answer starts.
- A program that sees `length` must know the answer is incomplete.
- Temperature 0 makes the answer repeatable, not correct. For a country it did
  not know, the toy model gave a single, wrong answer at temperature 0.
