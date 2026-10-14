| Term | Meaning |
|---|---|
| **Vague instruction** | An instruction that leaves length, content or form to the model |
| **Clear instruction** | An instruction that answers how much, what to contain, what not to contain, for whom and in what form |
| **Measurable rule** | A rule code can check: number of words, number of sentences, a word that must appear |
| **Checker** | A function that says whether the answer follows the rules |
| **Delimiter** | A marker that keeps data apart from instructions: `<review>` tags, triple quotes |
| **Escaping** | Turning special signs in the data (`<`, `>`, `&`) into a harmless form |
| **Prompt injection** | An attack that changes the model's behaviour with an instruction hidden in the data |

**Keep in mind:**

- A clear instruction does not only guide the model; it also tells the
  program **what to reject**. In the lesson one of four example replies
  passed every rule and three failed at least one.
- Generate the prompt text and the checker from the same rules
  dictionary.
- With the naive wrapper the tag count became 2 when the data wrote the
  closing tag; with the escaping wrapper it was 1.
- When escaping, `&` is handled first; otherwise escapes such as `&lt;`
  break.
