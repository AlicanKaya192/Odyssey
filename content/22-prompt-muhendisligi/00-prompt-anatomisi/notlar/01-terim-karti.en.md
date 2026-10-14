| Term | Meaning |
|---|---|
| **Prompt** | All the messages sent to the model: instructions, context, input |
| **System message** | The message that gives the model its role and rules, sent again in every call |
| **User message** | The job or the user's question processed in this call |
| **Role** | Who the model acts as ("you are a support assistant") |
| **Task** | The job asked of the model ("put it into a category") |
| **Context** | Information the job needs: categories, rules, documents |
| **Format** | What the answer looks like ("the category name only") |
| **Example reply** | In this module, a reply written in advance; not a measurement of a model |
| **Parsing** | Getting the value the program will use out of the answer |
| **Validation** | Checking whether that value is one of the allowed values |

**Keep in mind:**

- The model fills a part you leave out with its own guess.
- In the lesson the strict parser accepted three of the six example
  replies and set three apart as `needs_review`; the lenient parser gave
  a single category even to a reply that hesitated between two.
- In the classification prompt 73–78% of the tokens of short
  messages were the fixed system message; that part is paid again in
  every call.
