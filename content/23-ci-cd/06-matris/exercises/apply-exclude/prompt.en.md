Write the function `apply_exclude(combos, exclude)`. It should remove the combinations that match **any** rule in the `exclude` list and return the rest in order.

A combination matches a rule if **every** key–value pair of the rule is the same in the combination. A rule does not have to be a full combination: `{"os": "windows-latest"}` matches every Windows combination.

**Expected output:**

```
{'os': 'ubuntu-latest', 'python': '3.12'}
{'os': 'ubuntu-latest', 'python': '3.13'}
{'os': 'windows-latest', 'python': '3.13'}
2
```
