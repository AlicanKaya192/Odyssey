| Term | Meaning |
|---|---|
| **Template** | Fixed text that builds the prompt in every call by putting in variables |
| **Placeholder** | The mark in a template where a variable goes: `{message}`, `$name`, `{{order_id}}` |
| **Escaping** | Doubling a character that clashes with the template mark: `{{` and `}}` |
| **Loud error** | An error that reports the problem before running (`substitute`, `KeyError`) |
| **Silent error** | Behaviour that carries on without reporting the problem (`safe_substitute`) |
| **One-pass filling** | A value that was put in is not scanned again |
| **Template version** | A number raised with every change of the template; written into the log |

**Keep in mind:**

- `str.format` took the `{"category": ...}` part of the JSON example for a
  variable and raised `KeyError`.
- `safe_substitute` left the missing `$order_id` in the prompt and said
  nothing.
- The version doing `replace` one after another filled the `{{order_id}}`
  in the customer's message; the one-pass `render` left the message as it
  was.
- Cutting the 62-word message to 24 words from the start lost the real
  request; cutting the middle kept it.
