`run_agent(script, question, max_rounds)` should send the `[user]` message
with `ChatClient(script)` and `tools=TOOLS`. If the reply has no tool
call, return `[text, round]`. If it has, add the assistant message
(`"content": ""`, `"tool_calls": ...`), add the result of `get_order` for
every call (`{"error": "unknown tool"}` for an unknown tool) in the `tool`
role with `json.dumps`, and ask again. If `max_rounds` rounds are used up,
`[None, max_rounds]`.

**Expected output:**

```
['It shipped on 2026-10-09.', 2]
[None, 3]
```
