# What Is Data Science?

You have finished Python Fundamentals. You can write variables, build loops,
read files and query a database. From this section on you will use those
things **to answer a question**.

Data science is, briefly, this: you have a pile of records and you want to
get one sentence out of it.

- 3,000 rows of sales records → *"Which city is losing sales?"*
- 50,000 lines of log file → *"When do the errors happen most?"*
- 800 student grades → *"Does attendance really affect the grade?"*

It starts with a sentence and ends with a sentence. Everything in between is
what this path is about.

## The flow

Almost every data task goes through the same five steps:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Question</b><br>what do I want to know</span>
    <span class="arrow">→</span>
    <span class="node"><b>Data</b><br>read it, pull it together</span>
    <span class="arrow">→</span>
    <span class="node"><b>Cleaning</b><br>missing, broken, duplicated</span>
    <span class="arrow">→</span>
    <span class="node"><b>Analysis</b><br>filter, group, compute</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Answer</b><br>a number, a chart, a decision</span>
  </div>
  <figcaption>Most of the time goes into the two middle boxes. The exciting part of the code is at the end, but the work is already done by then.</figcaption>
</figure>

None of these steps is magic. You can do all of them with the Python you
already know — and in this section that is exactly what you will do.

## What does data look like?

Nearly all data in data science is a **table**: rows and columns.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">row</span><span class="anat-body">one record — a student, a sale, a measurement</span></div>
    <div class="anat-row"><span class="anat-label">column</span><span class="anat-body">one attribute — name, city, score, date</span></div>
    <div class="anat-row"><span class="anat-label">cell</span><span class="anat-body">a single value — <code>"Ankara"</code>, <code>82</code></span></div>
  </div>
</figure>

In Python the most natural way to hold that table is **a list of
dictionaries**:

```python
students = [
    {"name": "Ada", "city": "Ankara", "score": 82},
    {"name": "Kerem", "city": "Izmir", "score": 74},
    {"name": "Mina", "city": "Ankara", "score": 91},
]
```

Each dictionary is a row, each key is a column. When you pull an Excel file,
the result of a database query or a CSV file into Python, this is usually
exactly the shape you get.

## First question: what is the average?

```python
total = 0
for student in students:
    total = total + student["score"]

average = total / len(students)
print(average)
```

```text
82.33333333333333
```

It works. But notice: **you wrote three lines to take an average.** That is a
lot for a simple question.

## Second question: what is the average in Ankara?

```python
ankara_scores = []
for student in students:
    if student["city"] == "Ankara":
        ankara_scores.append(student["score"])

average = sum(ankara_scores) / len(ankara_scores)
print(average)
```

```text
86.5
```

Works again. But one more question was asked and the code doubled.

## Third question: what is the average in every city?

```python
totals = {}
counts = {}

for student in students:
    city = student["city"]
    totals[city] = totals.get(city, 0) + student["score"]
    counts[city] = counts.get(city, 0) + 1

averages = {}
for city in totals:
    averages[city] = totals[city] / counts[city]

print(averages)
```

```text
{'Ankara': 86.5, 'Izmir': 74.0}
```

Ten lines. And that is for three rows of data.

## This is where the problem is

The code you wrote is not wrong. The problem is that **as the question grows,
the code grows** — and it is easy to make mistakes in growing code. If you
forget to update the `counts` dictionary the result is quietly wrong: the
program does not crash, it hands you a wrong number.

Then there is speed. At three rows it makes no difference, but at **three
million rows** a Python loop takes minutes.

There are two libraries for these two problems, and most of this path is
about learning them:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>NumPy</h4>
      <p>Arithmetic on arrays of numbers. It works on a whole array at once without a loop, and does it at C speed.</p>
    </div>
    <div class="versus-side">
      <h4>pandas</h4>
      <p>Working with tables. Reading, filtering, grouping, joining — all of it built in. Built on top of NumPy.</p>
    </div>
  </div>
</figure>

That ten-line city average above is this in pandas:

```python
data.groupby("city")["score"].mean()
```

One line. You will not be able to write that line yet by the end of this
section — but you will know exactly what it replaces. **You understand the
library because you did it by hand first.**

## Where do libraries come from?

`sqlite3` ships inside Python; NumPy and pandas do not. They are packages you
install separately:

```text
pip install numpy pandas
```

Odyssey takes care of this for you — the environment your exercises run in
already has them. When you build your own project you will use the virtual
environment approach from the `Modules` section.

## What you will do in this section

All five exercises are **without libraries**. You will take an average,
filter rows, pull out a column, group records and print a small summary
report — all in plain Python.

The point is this: when you write `mean()` in the next section, you will know
what is behind it. A library does not make the work easy for someone who does
not understand it; it saves time for someone who does.

## Summary

- Data science starts with a **question** and ends with data — not with code.
- The flow is always the same: question → data → cleaning → analysis →
  answer.
- Data is almost always a **table**: row = record, column = attribute.
- In Python a table is usually **a list of dictionaries**.
- Plain Python can do all of it, but the code grows fast and stays slow on
  large data.
- **NumPy** is for arrays of numbers, **pandas** for tables. Both are
  installed separately.
