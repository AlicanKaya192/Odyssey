`ask_json(script, max_tries)` should ask `QUESTION` with
`ChatClient(script)` (`max_tokens=60`). Check every answer with the given
`parse_json` and `validate`. If there are no errors return `[data, number
of tries, number of messages in the last call]`. If there are errors, add
the answer as an `assistant` message and the message built from the
errors (`"Your answer was not valid: "` + joined with `"; "` +
`". Reply with the JSON object only."`) as a `user` message and ask
again. If `max_tries` tries are used up,
`[None, max_tries, number of messages in the last call]`.

**Expected output:**

```
{'category': 'shipping', 'urgent': True}
3 5
None
2 3
```
