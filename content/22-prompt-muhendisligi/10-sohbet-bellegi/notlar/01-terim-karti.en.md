| Term | Meaning |
|---|---|
| **Stateless API** | A setup where the model does not remember earlier calls and the history is sent in every call |
| **Window** (last N messages) | Sending only the last messages of the history |
| **Summary** | Old messages shortened by a model call; may be lossy |
| **Fact memory** | Exact facts such as a name or an order number kept in a structured form |
| **Long-term memory** | A per-user record remembered in the next conversation too |
| **Storage filter** | A check that keeps information such as passwords and card numbers out of memory |

**Keep in mind:**

- In the lesson, over ten messages the whole history took 1565 tokens,
  the last four messages 695 and the last four messages + fact memory
  847; only the last four messages lost the order number.
- The example summary took four messages from 56 tokens to 23 but dropped
  the order number.
- The filter stored nothing from the messages with a password or a card
  number; regular expressions may still miss other spellings.
- Memory should be per user, visible, deletable and timed.
