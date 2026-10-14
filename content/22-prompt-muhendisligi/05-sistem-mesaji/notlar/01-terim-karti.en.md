| Term | Meaning |
|---|---|
| **System message** | The message that carries the role, tone and rules, put first in every call |
| **Role** | The assistant's job description: who it is and whom it serves |
| **Tone** | The way of speaking; checkable if written with a measure |
| **Limit** | The topics the assistant covers and does not cover |
| **Ban** | Something never done: a promise, a discount, sharing personal data |
| **Version digest** (hash) | A short fingerprint of the system message; shows which version gave an answer |
| **Answer check** | Checking with code whether the system message's rules were kept in the answer |

**Keep in mind:**

- Models are trained to give the system message priority, but this is
  not a guarantee.
- In the lesson one of five example replies followed every rule; two
  contained a promise, one of them given to a message in which the user
  tried to override the role.
- Changing even a single number changed the version digest completely.
- Treat the system message as public; nothing secret is written in it.
