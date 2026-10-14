| Written | Result | Correct |
|---|---|---|
| `python-version: 3.10` | Read as a number, becomes `3.1` | `python-version: "3.10"` |
| A tab in the indentation | The reader stops: a tab character cannot start anything | Spaces only |
| `with:` in the same column as the step's `-` | The reader stops; `with` is not part of the step | `with:` in the same column as `uses:` |
| `runs-on:ubuntu-latest` | No space after the colon: not read as a key | `runs-on: ubuntu-latest` |
| Steps without `-` | A dictionary instead of a list | Each step starts with `- ` |
| `run: echo a: b` | The second colon may be taken for a new key | Quote the command or use <code>run: &#124;</code> |

**Reading the indentation**

```yaml
jobs:            # 0 spaces
  test:          # 2 spaces: inside jobs
    runs-on: x   # 4 spaces: inside test
    steps:       # 4 spaces: inside test
      - uses: y  # 6 spaces: an item of the steps list
        with:    # 8 spaces: part of the same step
          k: v   # 10 spaces: inside with
```

To find what a key belongs to, look upwards for the first line that is
indented **less** than it.

**What does the reader's message say?**

- `found character '\t'`: there is a tab somewhere.
- `expected <block end>` or `mapping values are not allowed here`: the
  indentation has shifted, or there is no space after a colon.
- The line number in the message is where the problem was **found**; the
  real mistake is often a line or two above.
