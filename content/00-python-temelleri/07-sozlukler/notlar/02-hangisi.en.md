You now know four data structures. Which one to pick is a decision that will
come up constantly while you write code. This note is here to make it easier.

## The four side by side

| | List | Tuple | Dictionary | Set |
|---|---|---|---|---|
| Written as | `[1, 2]` | `(1, 2)` | `{"a": 1}` | `{1, 2}` |
| Ordered | yes | yes | keeps insertion order | no |
| Can change | yes | **no** | yes | yes |
| Allows duplicates | yes | yes | keys cannot repeat | **no** |
| Access | `x[0]` | `x[0]` | `x["name"]` | no access by position |

## Three questions to decide

**1. Will you look something up by name?** Then a dictionary. A job like "find
the score for this username" means scanning from start to end every time in a
list.

**2. Does order matter?** If it does, a list or a tuple. The order of questions
in an exam matters; the tags on a product do not.

**3. Are duplicates a problem?** If they are, a set. "Which words appear in this
text" is answered by a set; "how many times does each appear" is answered by a
dictionary.

## Situations you will meet often

**Dropping duplicates from a list:**

```python
names = ["Ada", "Bob", "Ada", "Cem"]
unique = list(set(names))
```

Careful: because a set is unordered, the order of the resulting list can be
scrambled. If order matters, this is not the right method.

**Counting how many times something appears:**

```python
votes = ["python", "go", "python"]

counts = {}
for vote in votes:
    counts[vote] = counts.get(vote, 0) + 1

print(counts)     # {'python': 2, 'go': 1}
```

The `counts.get(vote, 0)` shape earns its keep here: it starts from zero when
the key is missing and adds to it when it is there. No `if` needed.

**Pairing two lists:**

```python
names = ["Ada", "Bob"]
scores = [90, 85]

pairs = dict(zip(names, scores))
print(pairs)     # {'Ada': 90, 'Bob': 85}
```

## Nesting

These can sit inside one another, and in real programs they constantly do:

```python
students = [
    {"name": "Ada", "grades": [90, 85]},
    {"name": "Bob", "grades": [70, 75]},
]

print(students[0]["name"])         # Ada
print(students[0]["grades"][1])    # 85
```

You read left to right: `students[0]` gives you the first dictionary, `["name"]`
gives you its name. It looks complicated, but the rule never changes.
