The path of a single call to a chat API, with the pieces we built in the
section:

1. **The program prepares the message list.** The system message, every
   earlier user and assistant message, and the new question. Since the API is
   stateless, the history is sent from the start every time.
2. **The template is applied.** The list is turned into a single token
   sequence with role markers and the assistant marker is added at the end.
3. **The model generates token by token.** At every step the distribution of
   the next token is computed and a token is chosen according to settings such
   as the temperature.
4. **Generation stops.** `stop` if the stop marker comes, `length` if
   `max_tokens` is reached.
5. **The answer returns.** The text, the finish reason and how many tokens
   were processed.

**What to do on the program side:**

- Look at the finish reason: if it is `length` the answer is incomplete;
  either raise the limit or mark the answer as incomplete.
- **Check** the answer: the model can give a fluent but wrong answer. Compare
  it with a source, a rule or a test.
- Keep the temperature low if you need repeatability; but for correctness rely
  on checking, not on the temperature.
- Asking the same question a few times shows whether the answer is
  consistent; inconsistency is a sign of weak grounding.

**Common mistakes:**

- **Not sending the earlier messages** and expecting the model to "remember".
- **Ignoring `length`:** a half answer is used as if it were complete.
- **Mistaking temperature 0 for correctness.** At temperature 0 the toy model
  also gave the capital of the wrong country.
- **Building the template wrongly by hand:** without the assistant marker the
  model continues the dialogue instead of answering.
