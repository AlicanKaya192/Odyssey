The jobs are in a dictionary: the key is the job's name, the value the list of jobs it waits for.

Write the function `unknown_needs(needs)`. For every case where a job waits for a job that does not exist, return the text `"job -> awaited"` in a list, in order. If there is no problem, an empty list.

- If `"build": ["lint", "tests"]` and there is no job called `tests`: `"build -> tests"`

**Expected output:**

```
['build -> tests', 'deploy -> approve']
[]
```
