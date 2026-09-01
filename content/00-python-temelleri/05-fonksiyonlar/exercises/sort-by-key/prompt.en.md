`sorted` sorts a list, but when the elements are dictionaries it cannot answer
"which one is bigger". `key` answers exactly that question.

The data you have:

```python
people = [
    {"name": "Grace", "grade": 75},
    {"name": "Ada", "grade": 90},
    {"name": "Brian", "grade": 40},
]
```

**What you need to do:**

1. Write a function called `by_grade`: it takes a dictionary and returns its
   `grade` value.
2. In a variable called `best_first`, hold the people sorted by **grade,
   highest first**. Give `sorted` both `key` and `reverse`.
3. In a variable called `names`, hold the **names** in that order as a list.
4. In a variable called `alphabetical`, hold the names sorted alphabetically
   as a list.
5. Print `names` first, then `alphabetical`.

**Expected output:**

```
['Ada', 'Grace', 'Brian']
['Ada', 'Brian', 'Grace']
```

Note: you write `key=by_grade`, not `key=by_grade()`. You are giving it the
function itself, not its result.

> Add `reverse=True` to sort from largest to smallest.
