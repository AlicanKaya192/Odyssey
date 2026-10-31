Write `#[tag(label)]`: each time the function is called, it first prints `[label] name`, then runs the body. The label comes from the first input, the name from the token after `fn`.

**Expected output:**

```text
[db] load
1
[net] send
2
```
