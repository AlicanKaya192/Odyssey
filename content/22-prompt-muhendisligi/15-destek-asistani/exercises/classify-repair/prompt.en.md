`classify_with_repair(script, message)` should send `[system (CLASSIFY),
user]` with `ChatClient(script)` (`max_tokens=20`). If the answer cannot be
parsed with the given `parse_label`, it should add the model's answer and
the user message `"Only the category word, please."` to the messages and
ask once more. Return `[category or None, number of calls]`.

**Expected output:**

```
['payment', 1]
['payment', 2]
[None, 2]
```
