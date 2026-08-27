```python
numbers = [10, 20, 30, 40, 50, 60]
```

Take two slices:

| Variable | What it holds |
|---|---|
| `middle` | three items, starting at index 1 and **including** index 3 |
| `last_two` | the **last two** items of the list |

Print both, one under the other. Expected output:

```
[20, 30, 40]
[50, 60]
```

> Remember: in a slice **the end index is excluded**. To get three items you
> have to write one more as the end.
