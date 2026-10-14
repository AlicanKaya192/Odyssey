`render_chat(messages)` should turn the message list into a single text: for
every message a `<role>` marker and the content, separated by single spaces;
`<assistant>` at the end. For example for
`[{"role": "user", "content": "hi !"}]`: `"<user> hi ! <assistant>"`.

**Expected output:**

```
<system> be brief . <user> hi <assistant>
```
