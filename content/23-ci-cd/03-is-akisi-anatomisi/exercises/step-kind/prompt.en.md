A step is a dictionary. Write the function `step_kind(step)`:

- If it has both `uses` and `run`: `"invalid"`
- If it has only `uses`: `"action: "` + the action's name
- If it has only `run`: `"command: "` + the **first line** of the command
- If it has neither: `"invalid"`

The lines of a multi-line `run` text are separated by `"\n"`.

**Expected output:**

```
action: actions/checkout@v4
command: python -m pytest
command: pip install -U pip
invalid
invalid
```
