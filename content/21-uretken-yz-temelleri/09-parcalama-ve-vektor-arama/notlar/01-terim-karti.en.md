| Term | Meaning |
|---|---|
| **Chunk** | A small part of a document that is searched and sent to the model |
| **Chunking** | The way a document is split: per article, per sentence, a fixed window |
| **Overlap** | The words consecutive chunks share; it reduces splitting at a border |
| **Vector search** | Finding the chunks whose vectors are closest to the question |
| **Cosine similarity** | How alike two vectors' directions are; the dot product for vectors of length 1 |
| **Embedding model** | A model that turns text into a numeric vector reflecting its meaning |
| **Vector database** | A system that stores many vectors and does approximate nearest neighbour search |
| **Hybrid search** | Using word search and embedding search together |
| **key@k** | The share of questions whose answer phrase appears in one of the first k chunks |

**Keep in mind:**

- In the section the whole article gave 1.0 / 225 tokens, sentences 0.71 / 50
  tokens, 24 words + 8 overlap 0.88 / 106 tokens.
- Word search misses a question asked in other words ("money back" vs
  "refund").
- Chunking and search are chosen by measuring with real questions.
