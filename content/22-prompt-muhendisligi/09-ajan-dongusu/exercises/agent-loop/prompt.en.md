`agent(script, question, max_steps)` should build the loop of the
lesson: `ChatClient(script)`; in every round ask with `tools=SCHEMA` and
add `input_tokens` to the trace. If there is no tool call, return
`[answer, round, trace]`. If there is, add the `assistant` message; for
each call, if the same call (`json.dumps(call, sort_keys=True)`) came
before, `{"error": "you already made this call"}`, otherwise the given
`run_tool` result is added as a `tool` message. If `max_steps` rounds are
used up, `[None, max_steps, trace]`.

**Expected output:**

```
It is being prepared. 2
[37, 57]
None 3
[37, 57, 80]
```
