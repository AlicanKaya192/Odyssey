`check_call(call, specs)` should check a tool call; `specs` maps a tool
name → `{argument: pattern}`. In order: if the tool is not in `specs`,
`"unknown tool <name>"`; if the set of argument names is not the expected
one, `"arguments must be "` + the expected names joined with `", "`; if an
argument does not match its pattern with `re.fullmatch`, `"<argument> has
the wrong form"`; if all pass, `"ok"`. If the call has no `arguments`,
treat it as an empty dictionary.

**Expected output:**

```
ok
arguments must be order_id
order_id has the wrong form
unknown tool refund
```
