# Dictionaries and Sets

In a list you reached each item **by its index**. But what if what you have is
not a sequence, it is a pairing? A country and its capital, a product and its
price, a username and their score.

That is what a dictionary is for: you store values not by a number, but under
**a name you choose yourself**.

## Creating a dictionary

Open a curly bracket and write each pair as `key: value`:

```python
capitals = {"Turkey": "Ankara", "France": "Paris", "Japan": "Tokyo"}
```

Writing longer dictionaries one line at a time makes them easier to read:

```python
prices = {
    "apple": 12,
    "banana": 8,
    "cherry": 45,
}
```

The trailing comma is not a mistake, it is deliberate: when you add a new line
you do not have to touch the one above it.

## Keys and values

The left side of each pair is the **key**, the right side is the **value**.
Keys are usually text but can be numbers. A value can be anything — a number,
some text, even a list:

```python
student = {
    "name": "Ada",
    "age": 20,
    "grades": [90, 85, 78],
}
```

## Reading a value

You use square brackets, but inside them you write a **key**, not an index:

```python
capitals = {"Turkey": "Ankara", "France": "Paris"}

print(capitals["Turkey"])     # Ankara
```

Ask for a key that is not there and you get an error:

```python
print(capitals["Spain"])
# KeyError: 'Spain'
```

## Is the key there?

`in` works here just as it did with lists — but it looks at the **keys**, not
the values:

```python
print("Turkey" in capitals)     # True
print("Ankara" in capitals)     # False   <- that is a value, not a key
```

So the safe way to read is:

```python
if "Spain" in capitals:
    print(capitals["Spain"])
else:
    print("not found")
```

## Adding and changing

Both are done with the same line. If the key is not there it is **added**; if
it is, its value **changes**:

```python
capitals = {"Turkey": "Ankara"}

capitals["Japan"] = "Tokyo"       # a new pair was added
capitals["Turkey"] = "ANKARA"     # an existing value changed

print(capitals)     # {'Turkey': 'ANKARA', 'Japan': 'Tokyo'}
```

There is no separate method like the list's `append`; assignment is enough.

## Removing

```python
del capitals["Japan"]
```

## Length and looping

`len()` gives the **number of pairs**:

```python
print(len(capitals))     # 1
```

When you loop over a dictionary, what you get is the **keys**:

```python
prices = {"apple": 12, "banana": 8}

for key in prices:
    print(key, prices[key])

# apple 12
# banana 8
```

The cleaner way to get both key and value is `items()`:

```python
for key, value in prices.items():
    print(key, value)
```

## Sets

A set is also written with curly brackets, but it holds single **values**, not
pairs:

```python
tags = {"python", "data", "python", "web"}

print(tags)          # {'python', 'data', 'web'}
print(len(tags))     # 3
```

It has two properties: it **holds no duplicates** and it is **unordered**.
Above, "python" was written twice but appears once. Because it is unordered
there is no such thing as `tags[0]` — you cannot reach items by index.

Its most common use is dropping duplicates from a list:

```python
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)

print(unique)     # {1, 2, 3}
```

## The empty trap

There is one thing to watch here:

```python
empty_dict = {}          # this is an EMPTY DICTIONARY
empty_set = set()        # this is how you write an empty set
```

`{}` is not an empty set, it is an **empty dictionary**. For an empty set you
have to write `set()`. In Python, curly brackets belong to dictionaries first.

## Which one, when?

| What you need | Structure |
|---|---|
| An ordered collection that can change | **list** `[ ]` |
| An ordered collection that must not change | **tuple** `( )` |
| A name-to-value pairing | **dictionary** `{k: v}` |
| A collection with no duplicates | **set** `{a, b}` |

---

## Summary

- A dictionary stores values under a **key**, not an index.
- You read with `my_dict[key]`; a missing key raises a `KeyError`.
- `in` looks at the **keys**, not the values.
- Assignment both adds and updates: `my_dict[key] = value`.
- Looping over a dictionary gives you the keys; `items()` gives you both.
- A set holds no duplicates and is unordered; `set(my_list)` is the short way
  to drop duplicates.
- `{}` is an empty **dictionary**; an empty set is written `set()`.
