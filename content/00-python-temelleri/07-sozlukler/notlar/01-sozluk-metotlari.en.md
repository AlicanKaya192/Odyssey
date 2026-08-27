Dictionaries have their own methods too. Knowing five of them is enough.

## get — reads without raising

```python
prices = {"apple": 12, "banana": 8}

print(prices.get("apple"))       # 12
print(prices.get("cherry"))      # None   <- no error
```

This is where it differs from square brackets: `prices["cherry"]` raises a
`KeyError`, while `get` quietly returns `None`.

Give it a second value and it returns that when the key is missing:

```python
print(prices.get("cherry", 0))     # 0
```

You will use this shape a lot: "take its value if it is there, otherwise count
it as zero".

## keys, values, items

```python
prices = {"apple": 12, "banana": 8}

print(list(prices.keys()))       # ['apple', 'banana']
print(list(prices.values()))     # [12, 8]
print(list(prices.items()))      # [('apple', 12), ('banana', 8)]
```

`items()` gives each pair as a **tuple**. This is the form you will use most in
loops:

```python
for key, value in prices.items():
    print(key, "->", value)
```

## update — adds and updates in bulk

```python
prices = {"apple": 12}
prices.update({"banana": 8, "apple": 15})

print(prices)     # {'apple': 15, 'banana': 8}
```

It updates keys that exist and adds ones that do not. Use it when you want to
hand over several pairs at once instead of assigning them one by one.

## setdefault — adds only if missing

```python
prices = {"apple": 12}

prices.setdefault("apple", 99)     # apple is already there, LEAVES IT
prices.setdefault("cherry", 45)    # cherry is missing, adds it

print(prices)     # {'apple': 12, 'cherry': 45}
```

People mix this up with `update`. The difference in one sentence: **`update`
overwrites, `setdefault` does not.**

## A word of warning

In some material you will see claims like "what you add with setdefault is not
permanent". That is true but misleading — **nothing** you add to a dictionary,
by any means, is permanent. When the program closes, everything in memory goes.
If you want it to last you have to write it to a file or a database; this is
not a limitation of `setdefault`.

## Dictionary or list?

When you are searching for something, the difference matters:

```python
# searching a list: it looks from start to end
if "apple" in fruit_list:
    ...

# searching a dictionary: it goes straight there
if "apple" in prices:
    ...
```

The bigger the list, the slower the search; in a dictionary the search speed
does not change with size. If your job sounds like "find this one by name", a
dictionary is the right choice.
