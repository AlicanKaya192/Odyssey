`classify_all(texts)` should classify every text with a separate call:
create `ChatClient(SCRIPT)`; for each text send the list `[system, user]`
(`SYSTEM` and the text) with `max_tokens=5`, `temperature=0.0` and parse
the answer with the given `parse_label`. Return `[list of labels, number
of calls, number of calls whose first message is system]`; count the
calls from `client.calls`.

**Expected output:**

```
['shipping', 'warranty', 'needs_review']
3 3
```
