Slicing is one of the most useful things about lists. Once the rule clicks, you
will find it works exactly the same way on text.

## The basic form

```python
list[start:end]
```

**The start is included, the end is not.** That one sentence is half of slicing.

```python
numbers = [0, 1, 2, 3, 4, 5]

print(numbers[2:5])     # [2, 3, 4]     no 5
```

The rule may look odd, but it has a benefit: `end - start` tells you directly
how many items you took. `numbers[2:5]` is three items.

## Leaving an end blank

```python
print(numbers[:3])      # [0, 1, 2]              from the start
print(numbers[3:])      # [3, 4, 5]              to the end
print(numbers[:])       # [0, 1, 2, 3, 4, 5]     everything
```

`list[:]` gives you a **copy** of the list. That matters, and we will come back
to it in a moment.

## With negative numbers

```python
print(numbers[-3:])     # [3, 4, 5]     the last three
print(numbers[:-1])     # [0, 1, 2, 3, 4]   everything but the last
```

You will use the `list[-3:]` shape a lot: "give me the last three".

## Step

A third number sets the step:

```python
print(numbers[::2])     # [0, 2, 4]     every other one
print(numbers[1::2])    # [1, 3, 5]     from 1, every other one
print(numbers[::-1])    # [5, 4, 3, 2, 1, 0]   reversed
```

`[::-1]` is the shortest way to reverse a list.

## Going past the end is not an error

Ask for an index beyond the end and you get an error, but slicing does not
complain:

```python
print(numbers[10])      # IndexError
print(numbers[2:100])   # [2, 3, 4, 5]   fine
print(numbers[100:])    # []             an empty list
```

Slicing quietly gives you whatever it has. Sometimes that helps, sometimes it
hides a bug — if an empty list is not what you expected, you have to check for
it.

## The copy question

Assigning a list to another variable does **not** make a copy; both names point
at the same list:

```python
a = [1, 2, 3]
b = a
b.append(4)

print(a)     # [1, 2, 3, 4]   a changed too
```

If you really want a separate copy, take a slice:

```python
a = [1, 2, 3]
b = a[:]
b.append(4)

print(a)     # [1, 2, 3]      a is untouched
print(b)     # [1, 2, 3, 4]
```

This is one of the behaviours that surprises beginners most. Worth remembering.
