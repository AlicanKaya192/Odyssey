`answer(script, question)` should send `[system, user]` with
`ChatClient(script)` (`SYSTEM`, `question`, `max_tokens=80`) and check the
answer with the given `review`. If the problems contain `"promise"`,
return `[HANDOVER, number of calls]` at once. If there are no problems,
`[answer text, number of calls]`. If there is only a length problem, add
the answer as an `assistant` message and `SHORTEN` as a `user` message
and ask once more; if the second answer fails too,
`[HANDOVER, number of calls]`.

**Expected output:**

```
1 It left yesterday.
2 It left today.
1 A colleague will get back to you soon.
```
