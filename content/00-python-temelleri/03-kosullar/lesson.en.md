# Conditionals

Until now, every piece of code you wrote ran from top to bottom in the same order. Conditionals change that: they let a program take different paths depending on the situation.

## if

The simplest form: if a condition is true, do something.

```python
age = 20

if age >= 18:
    print("You can vote.")
```

The `if` line ends with a colon, and the block underneath is indented. If the condition is false, that block never runs and the program carries on.

## else

When you want to do something else if the condition is false:

```python
age = 15

if age >= 18:
    print("You can vote.")
else:
    print("You cannot vote yet.")
```

`else` takes no condition of its own — it means "if none of the above".

## elif

When there are more than two possibilities, use `elif`. Working out a letter grade is a good example:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)   # B
```

The thing to watch here is the **order**. Python tries the conditions from top to bottom and **runs the first true one, then ignores the rest**.

So if `score = 95`, only the first line runs; `score >= 80` is never even tried. Write the conditions in the wrong order and you get a problem:

```python
# WRONG ORDER
if score >= 70:
    grade = "C"
elif score >= 90:
    grade = "A"    # this is never reached
```

Someone scoring 95 still gets a "C", because the first condition is already true. The rule: **write from the narrow condition to the broad one.**

## Combining conditions

The `and`, `or` and `not` you learned in the previous section earn their keep here:

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("You may enter.")
```

`and` wants both to be true; `or` says one is enough.

## Nested conditions

You can write an `if` inside another `if`:

```python
age = 25
has_ticket = False

if age >= 18:
    if has_ticket:
        print("You may enter.")
    else:
        print("You need a ticket.")
else:
    print("You are too young.")
```

It works, but nest too deeply and the code becomes unreadable. When you see more than three levels of nested `if`, there is usually a better way to write it.

## Truthiness

In Python, values other than `True` and `False` can be used as conditions. Empty things count as false:

```python
name = ""

if name:
    print("Hello", name)
else:
    print("The name is empty.")
```

An empty string, zero and an empty list all count as **false**; anything with content counts as true. This shortcut makes life easier once you are used to reading code.

---

## Summary

- `if` runs when the condition is true; its body is indented.
- `else` means "if none of the above" and takes no condition.
- `elif` handles more than two possibilities.
- Python runs the **first true condition** and ignores the rest — order matters.
- `and`, `or` and `not` combine several conditions.
