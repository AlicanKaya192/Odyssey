When YAML is read, a workflow becomes a nested dictionary. `WORKFLOW` is that dictionary, ready.

Write the function `job_summary(workflow)`. Return a list with a one-line text for each job, in order:

- `"test: windows-latest, 3 steps"`

That is: the job's name, its `runs-on` value and its number of steps.

- The jobs are in the `workflow["jobs"]` dictionary.
- `.items()` gives both the name and the value.

**Expected output:**

```
lint: ubuntu-latest, 2 steps
test: windows-latest, 3 steps
```
