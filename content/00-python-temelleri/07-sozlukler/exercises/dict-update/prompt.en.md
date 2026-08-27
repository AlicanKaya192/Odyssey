A stock dictionary is given:

```python
stock = {"apple": 10, "banana": 5}
```

Do two things:

- Add a **new product** called `cherry` with a count of `20`.
- **Update** the count of `apple` to `15`.

Then print the dictionary and how many kinds of product there are. Expected
output:

```
{'apple': 15, 'banana': 5, 'cherry': 20}
3
```

> In a dictionary, adding and updating are done with **the same line**:
> `stock[key] = value`. If the key is missing it is added, if it exists its
> value changes. There is no separate method like the list's `append`.
