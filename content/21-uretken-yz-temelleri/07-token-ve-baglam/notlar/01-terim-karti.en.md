| Term | Meaning |
|---|---|
| **Token** | A piece of text the model reads and produces |
| **Tokenizer** | The method that splits text into tokens; every model has its own |
| **Context window** | The most tokens one call can process (input + output) |
| **Input tokens** | The token count of all messages sent, role markers included |
| **Output tokens** | The token count of the answer the model produces |
| **`max_tokens`** | The most tokens reserved for the answer; it takes room in the window |
| **Trimming the history** | Not sending old messages to save tokens; it loses information |
| **Recorded reply** | An example reply written in advance; not a measurement of a model |

**Keep in mind:**

- The counter in this section is simplified: punctuation 1, a word 1 token per
  started group of four characters. Real counts change from model to model.
- With a stateless API the history is sent again in every call; the total
  token count grows with the square of the number of messages (1088 for eight
  messages, 4.5 times the last call).
- Cost = input × input price + output × output price. A long system message
  and needless history are paid again in every call.
