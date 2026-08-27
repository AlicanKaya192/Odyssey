Lists come with built-in methods. You do not need to memorise them all;
knowing the six most used ones is enough.

## append — adds to the end

```python
teams = ["Python", "Java"]
teams.append("Go")

print(teams)     # ['Python', 'Java', 'Go']
```

It adds one item and always puts it at the **end**. This is the method you will
reach for most.

## insert — adds where you want

```python
teams = ["Python", "Go"]
teams.insert(1, "Java")

print(teams)     # ['Python', 'Java', 'Go']
```

The first number is the index, the second is the value. The item at that index
and everything after it shifts one to the right.

## remove — deletes by value

```python
teams = ["Python", "Java", "Go"]
teams.remove("Java")

print(teams)     # ['Python', 'Go']
```

If the same value appears more than once it removes **only the first one**. Try
to remove a value that is not there and you get a `ValueError`.

## pop — deletes by index and hands it back

```python
teams = ["Python", "Java", "Go"]
last = teams.pop()       # with no index you get the last one
first = teams.pop(0)

print(last)      # Go
print(first)     # Python
print(teams)     # ['Java']
```

The difference from `remove`: `pop` **gives back** what it removed, `remove`
does not.

## sort — sorts the list

```python
numbers = [30, 10, 20]
numbers.sort()

print(numbers)     # [10, 20, 30]
```

It changes the list **in place** and does not produce a new one. For largest
first, use `numbers.sort(reverse=True)`.

With text it sorts alphabetically, but capitals come before lowercase letters —
sorting `["b", "A"]` gives `["A", "b"]`.

## count and index

```python
numbers = [10, 20, 10, 30]

print(numbers.count(10))     # 2   how many there are
print(numbers.index(20))     # 1   the position of the first one
```

## One thing to watch

Most of these methods change the list **in place** and return `None`. Here is a
common mistake:

```python
numbers = [30, 10, 20]
numbers = numbers.sort()     # wrong

print(numbers)     # None
```

`sort()` already sorted the list; assigning its result to the variable
overwrites the list with `None`. The correct line is simply `numbers.sort()`.
