A list of votes is given:

```python
votes = ["python", "go", "python", "rust", "go", "python"]
```

Count **how many votes each option got** and keep the result in a dictionary
called `counts`. Then print it. Expected output:

```
{'python': 3, 'go': 2, 'rust': 1}
```

The method: start with an empty dictionary, loop over the list, and add one to
the count for each vote. When the key is not there yet you have to start from
zero.

> The order of pairs in a dictionary is **the order they were first added**.
> Because `python` comes first in the list, then `go`, then `rust`, the output
> follows that order.
