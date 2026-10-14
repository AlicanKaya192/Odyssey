`allowed(tool, source, tools)` should say whether a tool request is
allowed: `False` if the tool is not in `tools`; if the tool's
`"irreversible"` value is `True`, `True` only when `source == "user"`;
reversible tools are `True` from every source.

**Expected output:**

```
get_order document True
cancel_order document False
cancel_order user True
refund user False
```
