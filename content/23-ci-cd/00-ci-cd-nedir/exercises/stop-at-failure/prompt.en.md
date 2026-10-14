The stages of a pipeline are given as a list of `(name, passed)` pairs:

- `("test", False)`: the `test` stage failed.

Write the function `run_pipeline(stages)`:

- Look at the stages in order.
- Return the **name** of the first failing stage; the pipeline stops there.
- If none of them failed, return `"passed"`.

The three lines below call your function and print the result.

**Expected output:**

```
test
passed
install
```
