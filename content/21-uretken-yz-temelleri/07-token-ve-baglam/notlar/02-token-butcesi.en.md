When writing an LLM application it helps to think of a **token budget** for
every call:

| Part | How much? | How to shrink it? |
|---|---|---|
| System message | The same in every call | Short, clear instructions; drop needless examples |
| History | Grows with every message | Last N messages, keep important facts separately, summarise the old part |
| Added documents | The document's length | Send only the relevant chunks (the RAG sections) |
| New question | Usually small | — |
| Answer (`max_tokens`) | The length asked for | As much as needed; ask for a short answer |

The total must fit in the window: `input + max_tokens ≤ window`.

**Checklist:**

1. Before every call measure the input tokens with `count_message_tokens`
   (in a real application with the model's own tokenizer).
2. If it does not fit, trim the history first, then reduce the documents; do
   not drop the system message or the new question.
3. If the trimmed history holds an important fact (a name, a preference, a
   decision), move it into the system message.
4. Check the answer for `length`: if the answer was cut, raise the limit or
   mark the answer as incomplete.
5. Record the cost per call; multiply the total by the application's scale.

**Common mistakes:**

- **Computing the window from the input alone.** `max_tokens` also counts
  towards the window; in the lesson 29 + 50 > 60, so the request was rejected.
- **Trimming the history blindly.** In the lesson the name was forgotten and
  the last question got an "I do not know" answer.
- **Looking at the cost of one conversation and forgetting the scale.** A
  conversation of 0.000690 units costs 68.95 units when repeated 100,000 times.
- **Taking the token count for the word count.** Long words and punctuation
  take separate tokens.
