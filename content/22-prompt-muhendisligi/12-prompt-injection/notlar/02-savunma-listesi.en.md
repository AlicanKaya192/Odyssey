A checklist for an LLM application's defence against injection:

| Layer | What is done? | What can it miss? |
|---|---|---|
| Separating data | Delimiter + escaping; saying "this is data, not instructions" | The model may still be influenced by a sentence in the data |
| Input detector | Patterns or a trained classifier | New spellings, other languages; raises false alarms |
| Least privilege | Only the tools needed | — (limits the harm, does not stop the attack) |
| Authority by source | A request from a document/tool cannot trigger an irreversible job | If the user themselves is the attacker |
| Confirmation | Human confirmation for irreversible jobs | If the human is careless |
| Output check | Canary, link allow-list, promise and secret patterns | Leaks that fit no pattern |
| Logging and monitoring | Log suspicious inputs and blocked outputs | — (makes it possible to notice later) |

**Rules:**

1. Treat the system message as public; write nothing secret in it.
2. Treat every outside text the model reads (a review, a document, a web
   page, a tool result) as untrusted data.
3. If you draw the answer on a page, filter links and images by an
   allow-list.
4. Keep the attacks you know and innocent messages that look like them in
   an evaluation set; measure again with every change.

**Common mistakes:**

- **Trusting a single layer.** In the lesson the detector missed three of
  seven attacks.
- **Thinking only of direct attacks.** In an indirect attack the user is
  innocent; the attack is in the data.
- **Granting authority on claims such as "I am the admin".** The real
  identity of the session decides authority.
- **Taking an image link for harmless.** The browser requests it by
  itself; data goes out without a click.
