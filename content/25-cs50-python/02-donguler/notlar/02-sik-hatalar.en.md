The most common mistakes in programs with loops and their messages (measured
on Python 3.14). Read the **last line** of an error message first.

## Going past the end of a list

```python
students = ["Hermione", "Harry", "Ron"]
print(students[3])
```

```text
$ python hogwarts.py
Traceback (most recent call last):
  File "hogwarts.py", line 2, in <module>
    print(students[3])
          ~~~~~~~~^^^
IndexError: list index out of range
```

A three-item list has positions 0, 1 and 2. The safe ways to reach the last
item are `len(students) - 1`, or simply `for student in students:`.

## A key that is not in the dict

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}
print(students["Luna"])
```

```text
$ python hogwarts.py
Traceback (most recent call last):
  File "hogwarts.py", line 7, in <module>
    print(students["Luna"])
          ~~~~~~~~^^^^^^^^
KeyError: 'Luna'
```

A dict has only the keys you defined. The spelling of a key must match
exactly too: `"harry"` and `"Harry"` are different keys.

## Giving range a string

```python
n = input("What's n? ")
for _ in range(n):
    print("meow")
```

```text
$ python cat.py
What's n? 3
Traceback (most recent call last):
  File "cat.py", line 2, in <module>
    for _ in range(n):
             ~~~~~^^^
TypeError: 'str' object cannot be interpreted as an integer
```

`input` returns a string, `range` needs an integer: `n = int(input(...))`.

## No `:` on the loop line

```python
for _ in range(3)
    print("meow")
```

```text
$ python cat.py
  File "cat.py", line 1
    for _ in range(3)
                     ^
SyntaxError: expected ':'
```

Like `if`, lines starting with `for` and `while` end with `:`.

## Mistakes without an error

These produce no message; the program runs but does not do what you want.

| What you wrote | What happens | Instead |
|---|---|---|
| no `i += 1` in the `while` body | the program never stops (`Ctrl+C`) | add the line that changes the condition |
| `while i <= 3` with `i = 0` | it runs four times | `i < 3`, or `i = 1` |
| counting 1 to `n` with `range(n)` | it counts 0 to `n - 1` | `range(1, n + 1)` |
| `print("#")` in the inner loop | each brick on its own line | `print("#", end="")` |
| the empty `print()` inside the inner loop | the line ends after every brick | `print()` in the outer loop |
| `for student in students:` on a dict, `print(student)` | only the keys are printed | `students[student]` for the value |
| `total = 0` inside the loop | the total resets on every iteration | start the counter **before** the loop |
