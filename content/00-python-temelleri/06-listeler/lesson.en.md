# Lists and Tuples

So far you have kept every value in its own variable. Three city names meant
three variables. But what if there were a hundred cities?

This is exactly what lists are for: they let you hold **more than one value in
a single variable**.

## Creating a list

Open a square bracket and separate the values with commas:

```python
cities = ["Istanbul", "Ankara", "Izmir"]
numbers = [10, 20, 30, 40]
empty = []
```

A list can hold values of **any kind**, and they can even be mixed:

```python
mixed = ["Python", 1991, True, 3.9]
```

In practice, putting things of the same kind together makes your life easier —
a list of scores, a list of names.

## Index numbers

Every item in a list has an **index**. And watch out here: **it starts at
zero.**

```python
cities = ["Istanbul", "Ankara", "Izmir"]

print(cities[0])     # Istanbul
print(cities[1])     # Ankara
print(cities[2])     # Izmir
```

In a list of three, the last item is number 2. Ask for an index that does not
exist and you get an error:

```python
print(cities[3])
# IndexError: list index out of range
```

## Counting from the end

A negative index counts from the end. This is very handy when you do not know
how long the list is:

```python
print(cities[-1])    # Izmir      the last item
print(cities[-2])    # Ankara     second from the end
```

Writing `cities[-1]` is both shorter and clearer than
`cities[len(cities) - 1]`.

## Taking a slice

With a colon you can take a **range**:

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:3])     # [20, 30]
print(numbers[:2])      # [10, 20]     from the start
print(numbers[2:])      # [30, 40, 50] to the end
```

The rule here is: **the start is included, the end is not.** `numbers[1:3]`
gives you items 1 and 2, but not item 3. The same logic as `range()`.

Taking a slice produces a new list; it does not touch the original.

## Changing an item

Lists are **mutable**. You can replace an item using its index:

```python
cities = ["Istanbul", "Ankara", "Izmir"]
cities[1] = "Bursa"

print(cities)     # ['Istanbul', 'Bursa', 'Izmir']
```

## Adding and removing

The method you will use most is `append` — it adds to the **end** of the list:

```python
cities = ["Istanbul", "Ankara"]
cities.append("Izmir")

print(cities)     # ['Istanbul', 'Ankara', 'Izmir']
```

To remove, use `remove` (by value) or `pop` (by index):

```python
cities.remove("Ankara")     # removes by value
cities.pop(0)               # removes the item at that index
```

## Length and searching

`len()` gives the number of items, and `in` tells you whether something is in
the list:

```python
cities = ["Istanbul", "Ankara", "Izmir"]

print(len(cities))              # 3
print("Ankara" in cities)       # True
print("Konya" in cities)        # False
```

Because `in` produces a **truth value**, it goes straight into an `if`:

```python
if "Ankara" in cities:
    print("it is in the list")
```

## Looping over a list

The structure you saw in the Loops section works here too:

```python
for city in cities:
    print(city)
```

If you also need the index, `enumerate` is the tool, but you do not need it yet.

## Tuples

A tuple is the **immutable** version of a list. Instead of square brackets you
use normal brackets:

```python
point = (3, 5)
colors = ("red", "green", "blue")

print(point[0])     # 3
```

Every way of reading it is the same as a list: index, negative index, slice,
`len`, `in`, looping. But you cannot change it:

```python
point[0] = 10
# TypeError: 'tuple' object does not support item assignment
```

**Why would we want that?** Two reasons. First, if you make something a tuple
it cannot be changed by accident — a coordinate, a date, a setting. Second,
whoever reads the code gets the message "this will not change" for free.

---

## Summary

- A list holds several values in one variable: `[1, 2, 3]`.
- Indexes start at **zero**; `-1` gives you the last item.
- When slicing, **the start is included and the end is not**: `numbers[1:3]`.
- Lists are mutable; `append`, `remove` and `pop` grow and shrink them.
- `len()` gives the length, `in` says whether something is inside.
- A tuple is written with `( )` and cannot be changed; reading it works like a list.
