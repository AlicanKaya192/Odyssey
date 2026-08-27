# Getting Started

This section is a short introduction to Python and to this application. Knowing what you are dealing with before you write code makes everything easier.

## What is Python?

Python is a programming language created by Guido van Rossum in 1991. One thing was put first in its design: **readability.**

Look at two pieces of code that do the same job. First Java:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

Then Python:

```python
print("Hello")
```

That difference is a real advantage for someone starting out. Instead of wrestling with the rules of the language, you get to think about the problem you are trying to solve.

## Why Python for data science?

Three reasons.

**The libraries are mature.** NumPy for numerical computing, pandas for data handling, scikit-learn for machine learning — all developed over many years. Writing them from scratch would take years.

**The community is large.** The answer to almost any problem you hit is out there somewhere. When you get stuck, you are not on your own.

**Prototype and production in one language.** You can try an idea quickly and, when it works, take it to production without switching languages.

## An interpreted language

Python is **interpreted**: your code runs line by line, with no separate compilation step. That makes experimenting easy — write a line, see the result immediately.

The trade-off is that it is slower than compiled languages like C or Rust. But in data science the heavy computation is done by libraries like NumPy, whose core is written in C. In practice you rarely feel that slowness.

## print() — your first command

The way to put something on the screen is `print()`:

```python
print("Hello")
```

You put what you want to print inside the brackets. Text goes in quotes, numbers do not:

```python
print("Hello")   # text   -> quotes needed
print(42)        # number -> no quotes
```

## Comments

Anything after a `#` is never read by Python. Comments are for leaving notes to yourself or to whoever reads your code:

```python
# This line does not run; it is only an explanation
print("This one runs")   # you can also write at the end of a line
```

In the exercises in this application you will see comments in the starter code — they tell you what to do.

## How this application works

Every section has four parts:

**Lesson** — the page you are reading now. You can jump anywhere using the heading list on the right.

**Lecture Notes** — extra texts that go deeper. I kept the main lesson short and left the details there.

**Quiz** — multiple choice questions. The point is not to grade you; under every question there is an explanation of why that answer is correct.

**Exercise** — where you write code. It runs your code and checks it: is your output right, did you define the right variable, did you use the structure that was asked for.

## About the exercises

If you get stuck, there are **three levels of hint**. The first nudges you, the second explains step by step, the third shows the solution. You decide how many to open — none of them opens by itself.

If your code raises an error, a box underneath explains **what it means**. Python's messages like `TypeError` are accurate but they do not teach; there you will find what happened and how to fix it.

> **Variable names are in English.** Every exercise in this application uses English names like `team`, `total`, `score`. There are two reasons: real Python code is written that way, and English keyboards have no Turkish characters.

## Progress

Your progress is stored on your own machine. When you complete a section it is marked on the path screen, and the code you wrote is still there when you close and reopen the app.

Sections are not locked — you can jump to any order you like, and go back to a section you finished to read it again.

---

## Summary

- Python is an interpreted language that puts readability first.
- It is preferred in data science for its mature libraries and large community.
- `print()` puts things on the screen; text goes in quotes.
- Lines starting with `#` do not run; they are for leaving notes.
- Every section has a lesson, lecture notes, a quiz and an exercise.
