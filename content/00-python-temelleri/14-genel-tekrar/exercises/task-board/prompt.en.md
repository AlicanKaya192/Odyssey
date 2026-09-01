You will use classes, lists and type annotations together.

**What you need to do:**

1. The `Task` class:
   - Its constructor takes `title` (a string) and `done` (a boolean,
     defaulting to `False`).
   - The `finish` method: sets `done` to `True` and returns nothing.
   - The `__str__` method: **returns** `[x] title` when it is done and
     `[ ] title` when it is not.

2. The `Board` class:
   - Its constructor creates an **empty** `tasks` list. Write the list's
     annotation: `list[Task]`
   - The `add` method: takes a `Task`, adds it to the list and returns the
     **total number** in the list.
   - The `pending` method: returns the **titles** of the unfinished tasks as a
     list. Its return annotation is `list[str]`.

3. Build a `Board` and add three tasks: `"write"`, `"test"`, `"ship"`. Finish
   the second one.
4. Print these in order: the number of tasks, the text form of the second
   task, and the pending titles.

**Expected output:**

```
3
[x] test
['write', 'ship']
```

> Create the `tasks` list **inside `__init__`**, not at class level.
