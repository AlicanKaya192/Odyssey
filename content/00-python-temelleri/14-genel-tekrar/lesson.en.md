# Overall Review

You are not learning anything new in this section. You are seeing how what you
have learned fits together.

Fourteen sections ago you were writing `print("hello")`. Now you can read a
file, turn the data in it into objects, write it to a database, and work out
what happened when an error comes up.

## How does it all connect?

You learned the pieces one at a time, but in a real program they all work
together:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>File</b><br>data arrives</span>
    <span class="arrow">→</span>
    <span class="node"><b>Loop + condition</b><br>rows are processed</span>
    <span class="arrow">→</span>
    <span class="node"><b>Dict / class</b><br>it gains structure</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Database</b><br>it becomes permanent</span>
  </div>
  <figcaption>Each arrow is a section. Functions break this flow into pieces, error handling stops broken data halting it, and type annotations write down what each step expects.</figcaption>
</figure>

A concrete example — reading a line of data and processing it:

```python
def load_scores(path: str) -> dict[str, int]:
    scores: dict[str, int] = {}

    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                name, value = line.split(",")
                scores[name] = int(value)
    except FileNotFoundError:
        return {}

    return scores
```

There are **nine sections** in those ten lines: variables, operators,
conditions, loops, functions, dictionaries, error handling, type annotations
and file handling. None of them was enough on its own; together they do a job.

## What did you learn, section by section?

| Section | The key idea |
|---|---|
| Getting Started | Python is interpreted; it runs line by line |
| Variables | A value has a type, and the type decides its behaviour |
| Operators | `/` gives a decimal, `//` does floor division |
| Conditionals | An `elif` chain stops at the first condition that holds |
| Loops | `for` for a known count, `while` while a condition holds |
| Functions | `print` shows, `return` gives — they are different |
| Lists | Ordered, indexed from zero, and changeable |
| Dictionaries | Reached by key; the name matters, not the position |
| Modules | You take ready-made code with `import` |
| Handling Errors | Do not catch it if you cannot do anything about it |
| Type Annotations | A note, not a rule; it is never checked |
| Working with Files | `with` closes, `"w"` wipes, always write `encoding` |
| Object-Oriented | Write a class when data and behaviour belong together |
| Databases | No commit means no change |

## The eight most common mistakes

The traps that came up again and again across these sections:

1. **Confusing `=` and `==`.** One assigns, one asks.
2. **`print` where `return` was needed.** A function that prints gives back
   `None`.
3. **Indexes start at zero.** The third element is `[2]`.
4. **`"w"` wipes the file.** Use `"a"` if you are appending.
5. **Forgetting `strip()`.** A line from a file carries a `\n`.
6. **Forgetting `self.`.** An object's data is not a free variable.
7. **Forgetting `commit`.** The database change is lost.
8. **A bare `except`.** It swallows the errors you were not expecting too.

What they all have in common: **most of them raise no error** and simply
behave incorrectly. Which is why code running does not mean code is right.

## When do you use what?

The thing beginners struggle with most is deciding which of their tools to
reach for.

**What should hold the data?**

| Situation | Tool |
|---|---|
| A single value | A variable |
| Many values in order | A list |
| Values reached by name | A dictionary |
| A fixed group that will not change | A tuple |
| Data **and** behaviour together | A class |
| It must survive the program closing | A file or a database |

**A function or a class?**

If the object has something it needs to remember, write a class; if not, a
function. If nothing is written with `self.`, it should not be a class.

**A file or a database?**

If you read the data start to finish, a file is enough. If you are asking
"give me the ones matching this" or "group these by that", use a database.

## Making code readable

Code that works is not enough. Three months from now you have to be able to
open your own code and understand what it does.

- **Let names say what they are.** `total` rather than `x`, `scores` rather
  than `d`.
- **Let a function do one job.** If you cannot name it, it is probably doing
  two.
- **Let comments explain the `why`.** The code already says the `what`.
- **Put type annotations on signatures.** That is the only thing someone
  calling your function gets to see.

## What comes next?

Python Fundamentals is finished. What follows is not the language itself but
the work done with it:

- **Data Science** — fast arithmetic with NumPy, tables with pandas,
  visualisation. The file reading and dictionary knowledge from this section
  connects straight to it.
- **SQL** — `JOIN` is built on top of the `SELECT` and `WHERE` you learned
  here.
- **Machine Learning** — modelling. You do not start it without Data Science.
- **API** — getting data from other systems. Dictionaries and error handling
  are essential.
- **Docker** — running a project the same way on every machine.

This section's exercises are built accordingly: each one uses **more than one
section** at the same time. That is how real code is written too.

## Summary

- The pieces you learned do their job together, not alone.
- Most mistakes raise no error; code running does not mean code is right.
- Choosing the tool matters as much as knowing it: list or dictionary,
  function or class, file or database.
- Writing readable code is part of the job, not a decoration added afterwards.
- What comes next is not the language itself but the work done with it.
