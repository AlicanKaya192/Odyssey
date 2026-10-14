`trim_history(messages, keep, facts)` should keep the system messages, put
a memory message after them if `facts` is not empty (in the `system` role,
`"Known facts: "` + `"key: value"` parts in key order joined with
`"; "`) and add only the last `keep` of the non-system messages.

**Expected output:**

```
system | Be brief.
system | Known facts: order: ORD-48213
assistant | On 2026-10-09.
user | Thanks!
```
