Before opening a tool to the model, fill in this table:

| Question | Example: `get_order` | Example: `cancel_order` |
|---|---|---|
| What does it do? | Reads an order's status | Cancels an order |
| Can it be undone? | Reading changes nothing | No |
| Does it need confirmation? | No | Yes: the customer or an employee |
| Argument pattern | `ORD-` + 5 digits | `ORD-` + 5 digits |
| Whose data does it reach? | Only the order of the customer in the chat | The same |
| How does an error come back? | `{"error": ...}` | `{"error": ...}` or `{"pending": ...}` |

**Rules on the program side:**

1. Keep the tools in an allow-list; never run the name the model gives in
   any other way.
2. Validate the arguments against a pattern; a customer's text can be
   carried into an argument.
3. Limit the data a tool can reach: another customer's order must not come
   back (the program knows the identity of the customer in the chat, not
   the model).
4. Wait for confirmation for irreversible jobs; a person gives it, not
   the model.
5. Give errors back to the model as structured results; the program must
   not crash.
6. Log every tool call with its arguments and result.

**Common mistakes:**

- **Running every call the model asks for.** A tool call is a request.
- **Writing the description carelessly.** The model often decides which
  tool to pick by looking at the description.
- **Not comparing the tool's result with the answer.** The model may write
  a fact that is not in the result.
- **Making one tool do too much.** General tools such as "run any SQL"
  enlarge the attack surface; write narrow tools.
