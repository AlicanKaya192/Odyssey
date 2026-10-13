`route(text)` should return a dictionary:

- `"category"`: the prediction of the ready `pipe` (plain text, `str`)
- `"orders"`: the order numbers in the text (`ORD-` + five digits, with word
  boundaries)
- `"urgent"`: whether `"urgent"` appears in the lowercased text

**Expected output:**

```
category shipping
orders ['ORD-55120']
urgent True
```
