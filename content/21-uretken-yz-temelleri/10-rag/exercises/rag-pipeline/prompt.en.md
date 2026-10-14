The read-only `rag_tools.py` holds the lesson's pieces: `index`,
`build_messages`, `make_reader`. `answer(question, k)` should: find the chunks
with `index.search(question, k)`, build the messages with `build_messages`,
call `chat(messages, max_tokens=100)` on `ChatClient([make_reader(2)])`.
Return `[answer text, input tokens]`.

**Expected output:**

```
135
Gift cards are available for 25, 50 and
100 euros and are valid for 3 years. [1]
117
I could not find this in the sources.
```
