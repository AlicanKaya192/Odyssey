`answer(script, question)` should build the loop of the lesson: send
`[system, user]` with `ChatClient(script)` (`tools=SCHEMA`). If the answer
has tool calls, add the message
`{"role": "assistant", "content": "", "tool_calls": ...}` and, for each
call, a `tool` message whose content is the result of the given
`run_tool` turned into text with `json.dumps`, then ask again. Return
`[text of the last answer, list of the messages' roles, number of
calls]`.

**Expected output:**

```
Your order is being prepared.
['system', 'user', 'assistant', 'tool']
2
```
