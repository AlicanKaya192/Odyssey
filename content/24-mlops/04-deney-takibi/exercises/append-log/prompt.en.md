Write the lesson's log so that it takes the file path as a parameter:

- `load_runs(path)`: an empty list if the file doesn't exist; otherwise open every line with `json.loads` and return the list.
- `log_run(path, params, metrics)`: the number is the count of experiments in the file + 1. Turn the dictionary `{"run": ..., "params": ..., "metrics": ...}` into one line with `json.dumps`, open the file in **append** mode (`"a"`) and write it at the end with a line break. Return the number.

**Expected output:**

```
1
2
2 2 1
[]
```
