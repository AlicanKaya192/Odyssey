Three more advanced features of functions. You will rarely need to write
them, but you will constantly need to **read** them — they appear in every
library's signatures.

## `sorted` and `key` — sorted by what?

`sorted` sorts a list:

```python
print(sorted([3, 1, 2]))
print(sorted(["banana", "apple"]))
```

```
[1, 2, 3]
['apple', 'banana']
```

But what if the elements are dictionaries? Python cannot answer "which one is
bigger":

```python
people = [
    {"name": "Ada", "grade": 90},
    {"name": "Brian", "grade": 40},
]

sorted(people)
```

```
TypeError: '<' not supported between instances of 'dict' and 'dict'
```

`key` answers exactly that question: **a function that produces the value to
compare for each element.**

```python
def by_grade(person):
    return person["grade"]


print(sorted(people, key=by_grade))
```

```
[{'name': 'Brian', 'grade': 40}, {'name': 'Ada', 'grade': 90}]
```

For largest first, `reverse=True`:

```python
sorted(people, key=by_grade, reverse=True)
```

Note that what you give `key` is **not called**: you write `key=by_grade`, not
`key=by_grade()`. You are giving it the function itself, not its result.

## `lambda` — a function with no name

The `by_grade` function above is one line and is used nowhere else. There is a
short form for cases like that:

```python
print(sorted(people, key=lambda person: person["grade"]))
```

<figure class="fig anat">
  <div class="sig"><u class="m1">lambda</u> <u class="m2">person</u>: <u class="m3">person["grade"]</u></div>
  <ul class="legend">
    <li class="m1"><b>The keyword</b> — it stands in for <code>def</code>, and no name is given.</li>
    <li class="m2"><b>The parameter</b> — no brackets, and more can be added with commas.</li>
    <li class="m3"><b>The returned value</b> — no <code>return</code> is written; the expression is the result.</li>
  </ul>
</figure>

A `lambda` can hold **one expression**. No `if` block, no loop, no multiple
lines. If you need those, write a `def`.

Places it is used often:

```python
sorted(words, key=len)                        # by length
sorted(people, key=lambda p: p["name"])       # by name
sorted(scores.items(), key=lambda pair: pair[1])   # a dictionary by value
```

The third one is useful: that is the standard way of sorting a dictionary **by
its values**.

**Do not** give a `lambda` a name. Rather than `add = lambda a, b: a + b`,
write `def add(a, b):` — they do the same job, but the second shows the
function's name in error messages.

## `*args` — when you do not know how many

When it is not known in advance how many arguments a function will take:

```python
def total(*numbers):
    result = 0
    for number in numbers:
        result = result + number
    return result


print(total(1, 2))
print(total(1, 2, 3, 4))
```

```
3
10
```

The star means "collect the incoming arguments into a **tuple**". Inside the
function `numbers` becomes `(1, 2, 3, 4)`.

The name does not have to be `args`, but that is the convention; you will
always see it that way in libraries.

## `**kwargs` — named arguments

Two stars collect the arguments given by name into a **dictionary**:

```python
def describe(**details):
    for key in details:
        print(key, "=", details[key])


describe(name="Ada", city="London")
```

```
name = Ada
city = London
```

All three can be used together, and **the order is fixed**:

```python
def report(title, *values, **options):
    ...
```

Ordinary parameters first, then `*args`, and `**kwargs` last.

## Where will you meet them?

In library signatures. A plotting function, for example:

```python
def plot(x, y, *args, **kwargs):
    ...
```

That signature means "take two required values, then whatever else you like".
When you see `**kwargs` in documentation, you will read it as "I can pass
extra settings here by name".

## Summary

- `sorted(items, key=...)` says what to sort by; `key` is given the function
  **itself**.
- `lambda x: expression` is a nameless, single-expression function. It is not
  used for something you are going to name.
- `*args` collects arguments into a tuple, `**kwargs` collects named ones into
  a dictionary.
- The order is fixed: ordinary parameters → `*args` → `**kwargs`.
