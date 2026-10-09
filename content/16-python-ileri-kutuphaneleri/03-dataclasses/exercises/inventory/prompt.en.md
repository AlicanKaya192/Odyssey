The `Inventory` dataclass: `owner: str` and `items: dict[str, int]`.
Every object must have **its own** dictionary
(`field(default_factory=dict)`). The `add(name, count)` method adds the count
(starting from 0 if missing). The starter code shares the dictionary; look at
the output.

**Expected output:**

```
Inventory(owner='ada', items={'pen': 5})
Inventory(owner='alan', items={})
```
