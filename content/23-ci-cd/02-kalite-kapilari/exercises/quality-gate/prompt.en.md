The pipeline's gates wrote their measurements into a dictionary:

- `"syntax"`: the exit code of the syntax gate
- `"format"`: the exit code of the format gate
- `"lint_errors"`: the number of lint errors
- `"coverage"`: the coverage percentage

Write two functions:

- `failed_gates(results, min_coverage)`: return a list of the names of the closed gates, in this order: `"syntax"`, `"format"`, `"lint"`, `"coverage"`. A gate closes if its exit code is not `0`, if there are lint errors, or if coverage is below `min_coverage`.
- `gate_message(failed)`: `"PASS"` if the list is empty, otherwise something like `"FAIL: format, lint"`.

You can use `", ".join(the_list)` to join the names with a comma and a space.

**Expected output:**

```
[]
['format', 'lint', 'coverage']
PASS
FAIL: format, lint, coverage
```
