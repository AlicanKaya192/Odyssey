`schema(tools)` should build the list that goes to the model from the
tool dictionary: for each tool `{"name": name, "description":
description, "parameters": list of argument names}`. The argument
patterns do not go to the model; only the names. The order is the same as
in the dictionary.

**Expected output:**

```
get_order ['order_id']
order_total ['order_id', 'currency']
```
