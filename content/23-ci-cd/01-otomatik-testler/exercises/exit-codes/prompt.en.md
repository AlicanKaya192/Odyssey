The pipeline looks at each step's exit code. Write two functions:

`step_status(code)`:

- `0` → `"green"`
- `1` → `"red: tests failed"`
- `5` → `"red: no tests"`
- any other number → `"red: error"`

`pipeline_status(codes)`: the exit codes of the steps, in order, in a list. If all are `0`, return `"green"`. Otherwise stop at the first non-zero step and return this (steps are counted from 1):

- `"red at step 2 (red: tests failed)"`

**Expected output:**

```
green
red: tests failed
red: no tests
red: error
green
red at step 2 (red: tests failed)
red at step 3 (red: no tests)
```
