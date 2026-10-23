# Loops

The third week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. A loop is a way to do
something over and over again: instead of writing the same line many times,
you run a block as often as you need.

## Writing the same line three times

Let us open a file called `cat.py`; our cat meows three times:

```python
print("meow")
print("meow")
print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

It works, but if we wanted 500 meows, would we write 500 lines? As a
programmer, every place where you type the same thing over and over is a place
where your code can improve.

## While loops

The `while` loop exists in nearly every programming language: it runs a block
again as long as a condition is true. A first try:

```python
i = 3
while i != 0:
    print("meow")
```

This code **never stops**: on every iteration Python asks "is `i` not equal to
zero?", and since `i` stays 3, the answer is always yes. If you get stuck in
such an **infinite loop**, `Ctrl+C` in the terminal interrupts the program. To
fix it, let us reduce `i` by one on each pass:

```python
i = 3
while i != 0:
    print("meow")
    i = i - 1
```

```text
$ python cat.py
meow
meow
meow
```

One pass through the loop is called an **iteration**. We can also count from 1,
the way most people do:

```python
i = 1
while i <= 3:
    print("meow")
    i = i + 1
```

```text
$ python cat.py
meow
meow
meow
```

`i = i + 1` computes the right side and assigns the result to the name on the
left. Programmers, though, start counting at **0**; `i += 1` is a shorter way
of writing the same thing:

```python
i = 0
while i < 3:
    print("meow")
    i += 1
```

<figure class="fig"><div class="flow"><span class="node">i = 0</span><span class="arrow">→</span><span class="node">i &lt; 3 ?</span><span class="arrow">→</span><span class="node ok">if yes, "meow"</span><span class="arrow">→</span><span class="node">i += 1</span><span class="arrow">→</span><span class="node">i &lt; 3 again?</span></div><figcaption>The loop asks the condition again on every iteration; when <code>i</code> becomes 3 the answer is <b>no</b> and the loop stops. <code>i</code> takes the values 0, 1 and 2: it counts up to 3 but not through it.</figcaption></figure>

(In CS50's notes every line of the example starting with `i = 1` is indented
too far; written that way Python raises an `IndentationError`. Here it is the
version verified by running it.)

## For loops

To understand a `for` loop, let us first meet a new type: the **list**. Like a
grocery list or a to-do list; values between square brackets, separated by
commas: `[0, 1, 2]`. `for` goes over the items of a list one by one:

```python
for i in [0, 1, 2]:
    print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

`i` is first 0 and meows, then 1, then 2. Much cleaner than the `while`
version. But what if we wanted a million meows? Instead of typing the list we
use `range`; `range(3)` produces the values 0, 1 and 2 by itself:

```python
for i in range(3):
    print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

To see the values `i` takes, let us print it:

```python
for i in range(3):
    print(i)
```

```text
$ python cat.py
0
1
2
```

In the meowing version we never use `i`; Python just needs a place to keep the
counter. By convention such a variable is called `_` (an underscore); it means
"I do not need this value", and the program behaves the same:

```python
for _ in range(3):
    print("meow")
```

To stretch your mind a little: multiplying a string by a number repeats it.

```python
print("meow" * 3)
```

```text
$ python cat.py
meowmeowmeow
```

To put each `meow` on its own line we add a line break (`\n`) to it; `end=""`
turns off `print`'s own line break, which would otherwise leave an extra blank
line at the end:

```python
print("meow\n" * 3, end="")
```

```text
$ python cat.py
meow
meow
meow
```

## Validating user input with a loop

Loops are also used to **validate** the user's input: asking again until a
value of the right kind arrives. In Python the common pattern is built with
`while True`. Let us ask the user for a number of 0 or more:

```python
while True:
    n = int(input("What's n? "))
    if n < 0:
        continue
    else:
        break

print("n is", n)
```

```text
$ python cat.py
What's n? -2
What's n? 5
n is 5
```

There are two new keywords. `continue` skips the rest of the loop and goes on
to the next iteration; `break` leaves the loop right away. If `n` is negative,
`continue` asks again; otherwise `break` leaves the loop.

Here `continue` is actually redundant: if the condition fails, the loop goes
back to the top anyway. This time let us ask for a number **greater** than 0
and meow that many times:

```python
while True:
    n = int(input("What's n? "))
    if n > 0:
        break

for _ in range(n):
    print("meow")
```

```text
$ python cat.py
What's n? -1
What's n? 0
What's n? 2
meow
meow
```

At first glance `while True` looks like it would run forever, because `True` is
always true. But once `n` is greater than 0, `break` breaks out of the loop.

With what we learned in the past weeks, let us split the work into functions:

```python
def main():
    meow(get_number())


def get_number():
    while True:
        n = int(input("What's n? "))
        if n > 0:
            return n


def meow(n):
    for _ in range(n):
        print("meow")


main()
```

```text
$ python cat.py
What's n? 3
meow
meow
meow
```

The `return n` inside `get_number` ends both the loop and the function and
hands the value back to `main`; no `break` is needed.

## More about lists

Back to Hogwarts from *Harry Potter*. `hogwarts.py`:

```python
students = ["Hermione", "Harry", "Ron"]

print(students[0])
print(students[1])
print(students[2])
```

```text
$ python hogwarts.py
Hermione
Harry
Ron
```

A list's items are reached by position, and positions start at **0**:
`students[0]` is Hermione. Going over the same list with a loop is cleaner:

```python
students = ["Hermione", "Harry", "Ron"]

for student in students:
    print(student)
```

```text
$ python hogwarts.py
Hermione
Harry
Ron
```

Here we wrote `student` rather than `_`, because we use the variable in the
body.

## Length

`len` gives how many items a list has. To print each student's position next
to their name:

```python
students = ["Hermione", "Harry", "Ron"]

for i in range(len(students)):
    print(i + 1, students[i])
```

```text
$ python hogwarts.py
1 Hermione
2 Harry
3 Ron
```

`range(len(students))` gives the positions (0, 1, 2); since people count from
1, we wrote `i + 1`. Thanks to `len`, the code stays the same however long the
list grows.

## Dictionaries

A **dictionary** (`dict`) is a data structure that associates keys with
values. A list holds several values in order; a dict pairs each key with a
value. To assign students to houses we could use two lists:

```python
students = ["Hermione", "Harry", "Ron", "Draco"]
houses = ["Gryffindor", "Gryffindor", "Gryffindor", "Slytherin"]
```

That means promising the two lists always stay in the same order, which gets
cumbersome as they grow. With a dict, between curly braces `{}`:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

print(students["Hermione"])
print(students["Draco"])
```

```text
$ python hogwarts.py
Gryffindor
Slytherin
```

A list is reached by position (a number), a dict by key (here a name). Going
over a dict with `for` gives us the **keys**:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

for student in students:
    print(student)
```

To print both the name and the house, we reach the value with
`students[student]`; `sep=", "` puts a comma and a space between them:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

for student in students:
    print(student, students[student], sep=", ")
```

```text
$ python hogwarts.py
Hermione, Gryffindor
Harry, Gryffindor
Ron, Gryffindor
Draco, Slytherin
```

To keep more information about each student we build a **list of dicts**.
Draco has no patronus; in Python "no value" is written `None`:

```python
students = [
    {"name": "Hermione", "house": "Gryffindor", "patronus": "Otter"},
    {"name": "Harry", "house": "Gryffindor", "patronus": "Stag"},
    {"name": "Ron", "house": "Gryffindor", "patronus": "Jack Russell terrier"},
    {"name": "Draco", "house": "Slytherin", "patronus": None},
]

for student in students:
    print(student["name"], student["house"], student["patronus"], sep=", ")
```

```text
$ python hogwarts.py
Hermione, Gryffindor, Otter
Harry, Gryffindor, Stag
Ron, Gryffindor, Jack Russell terrier
Draco, Slytherin, None
```

## Mario

In the classic *Mario* game the hero jumps over bricks. Let us draw a text
version. A column of three bricks, with a loop and a function instead of copy
and paste:

```python
def main():
    print_column(3)


def print_column(height):
    for _ in range(height):
        print("#")


main()
```

```text
$ python mario.py
#
#
#
```

The column can grow as tall as we like; we did not hard-code the number. A
horizontal row:

```python
def main():
    print_row(4)


def print_row(width):
    print("?" * width)


main()
```

```text
$ python mario.py
????
```

The game's blocks have both rows and columns. To draw both we use a **nested**
loop: the outer loop runs for each row, the inner one for each brick in the
row. The inner `print("#", end="")` lines the bricks up side by side, and the
empty `print()` in the outer loop ends the row:

```python
def main():
    print_square(3)


def print_square(size):

    # For each row in square
    for i in range(size):

        # For each brick in row
        for j in range(size):

            # Print brick
            print("#", end="")

        # Print blank line
        print()


main()
```

```text
$ python mario.py
###
###
###
```

One more step of abstraction: let `print_row` draw each row:

```python
def main():
    print_square(3)


def print_square(size):
    for i in range(size):
        print_row(size)


def print_row(width):
    print("#" * width)


main()
```

```text
$ python mario.py
###
###
###
```

## Summing up

You now have another power among your Python abilities:

- The `while` loop, infinite loops and `Ctrl+C`
- The `for` loop, `range` and `_`
- Validating input with `while True`, `break` and `continue`
- Lists, positions (from 0) and `len`
- Dictionaries, keys and `None`
- Nested loops

## This week's problem set

The seven exercises in the **Exercise** tab practise this lecture's topics one
by one. The ones in the **Problem Set** tab are CS50's assignment for the week
(Problem Set 2):

| Problem | What it asks | Topic in the lecture |
|---|---|---|
| camelCase | `firstName` → `first_name` | going over a string with `for` |
| Coke Machine | ask for coins until 50 cents | `while`, a counter |
| Just setting up my twttr | drop the vowels | `for`, `in` |
| Vanity Plates | whether a plate meets the rules | a function returning a `bool`, `len` |
| Nutrition Facts | the calories of a fruit | a dict, access by key |

Some problems use a small method the lecture did not show (`isupper`,
`isalpha`, `isdigit`); they are written in the prompts as hints.

---

*This section is translated and adapted from week 2 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
