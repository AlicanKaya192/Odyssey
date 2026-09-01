# How to Read a Traceback

That long block of text printed when an error appears is called a
**traceback**. It looks frightening but it has a regular structure, and once
you can read it you find the spot in seconds.

## The structure

```
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    report = build_report(users)
  File "main.py", line 7, in build_report
    return summarize(data)
  File "main.py", line 3, in summarize
    return total / count
ZeroDivisionError: division by zero
```

It has three parts:

1. **The first line** is always the same: "most recent call last".
2. **The middle lines** are the chain of calls. Each pair shows one place:
   which file, which line, which function — and underneath it, that line.
3. **The last line** is the error itself: its type and its explanation.

## Read from the bottom up

The last line says what happened. The lines just above it are **where the
error actually appeared**.

In the example above:

- What happened? A division by zero.
- Where? `main.py` line 3, inside the `summarize` function.
- How did we get there? Line 12 called `build_report`, which called
  `summarize` on line 7.

The first place to look is the **second-to-last** group. Everything above it
only shows the route.

## Which one is your code?

Sometimes library files appear in the chain too:

```
  File "C:\Python314\Lib\json\decoder.py", line 355, in raw_decode
```

These are usually not the culprit. **Look at the lowest line that names one
of your own files** — the error mostly comes from a value you handed over
there.

## The reported line can mislead

Python sometimes points at the next line. An unclosed bracket is the best
example:

```python
print("total:", total
print("done")
```

```
  File "main.py", line 2
    print("done")
    ^^^^^
SyntaxError: invalid syntax
```

The error is reported on line 2 but the problem is the open bracket on line
1. Python thinks the first line is still going and gives up on the second.

**Rule: if you cannot find anything on the reported line, look at the one
above.**

## Making your own errors readable

The explanation you write with `raise` appears on the last line of the
traceback. Writing it well saves you time later:

```python
raise ValueError("age cannot be negative")
```

```
ValueError: age cannot be negative
```

A poor example:

```python
raise ValueError("error")
```

Seeing that line three months later, you will not know which value caused the
trouble. Include the value where you can:

```python
raise ValueError(f"age cannot be negative: {age}")
```

## Errors inside this application

In this application your exercise code runs in a separate process, and if an
error appears the traceback is shown to you in a trimmed form: the
application's own files are stripped out and the line from your code is
brought to the front.

So the line number you see on screen is the line number of **the code you
wrote**. When you run a file on your own computer you will see the full form
shown above.
