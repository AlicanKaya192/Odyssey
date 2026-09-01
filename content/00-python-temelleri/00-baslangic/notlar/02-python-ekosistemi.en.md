# The Python Data Science Ecosystem

In this section you are only writing `print`. But it helps to know where you
are heading — so here is the map.

You do not need to learn any of the following now. Recognising the names when
you hear them is enough.

## Why are there so many libraries?

Python itself is a small language. It adds numbers, handles text, reads
files. The data science work — processing millions of rows a second, drawing
charts, training models — is not part of the language. **Libraries** do that.

A library is ready-made code that someone else wrote and shared. You call it
with `import` and start using it.

## The order

The learning order is not arbitrary; each layer rests on the one below it.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Python</b><br>the language</span>
    <span class="arrow">→</span>
    <span class="node"><b>NumPy</b><br>numeric arrays</span>
    <span class="arrow">→</span>
    <span class="node"><b>pandas</b><br>tables</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>scikit-learn</b><br>models</span>
  </div>
  <figcaption>Each layer is built on the previous one. pandas uses NumPy internally, and scikit-learn uses both.</figcaption>
</figure>

## What is each one for?

| Library | What it does | When you will learn it |
|---|---|---|
| **NumPy** | Fast arithmetic over numeric arrays | Data Science path |
| **pandas** | Reading, filtering and grouping tables | Data Science path |
| **Matplotlib** | Drawing charts | Data Science path |
| **scikit-learn** | Machine learning models | Machine Learning path |
| **SQLite** | A database (it ships inside Python) | End of Python Fundamentals |

## A short preview

Today you take the average of a list of numbers like this:

```python
scores = [90, 70, 85]
average = sum(scores) / len(scores)
print(average)
```

```
81.66666666666667
```

The same job with pandas, but over an entire table:

```python
average = table["score"].mean()
```

The difference is not speed, it is **scale.** With three numbers the two are
the same. With three million rows the first takes minutes and the second
takes seconds.

But keep this in mind: to be able to write that second line you have to
understand what `table["score"]` is — and that is the dictionary and list
knowledge you will pick up in these sections.

## Where do they sit in the application?

There are six paths in the learning route:

- **Python** — you are here. The language itself.
- **Data Science** — NumPy, pandas, visualisation.
- **Machine Learning** — modelling, feature engineering.
- **SQL** — pulling data out of a database.
- **API** — getting data from other systems.
- **Docker** — running a project the same way on every machine.

Everything except Python is locked for now. The reason is simple: they all
require knowing Python.

## One warning

The most common mistake beginners make is skipping the fundamentals and
jumping straight to pandas. It looks like it is working — because copied
examples run. Then the first error message arrives and you have no idea what
to do.

Using pandas without knowing loops, conditions, functions and dictionaries is
like reading a book without knowing the alphabet.
