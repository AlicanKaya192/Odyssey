This exercise is a small version of a real job: read from a file, turn it
into objects, group it, sort it and report.

`students.txt` has been placed next to your code:

```
Ada,90,London
Brian,40,London
Grace,75,NewYork
Alan,60,London
Edith,95,NewYork
```

**What you need to do:**

1. The `Student` class: its constructor takes `name`, `grade` and `city`. The
   `is_passing` method returns `True` when the grade is 50 or above.

2. The `load_students` function: takes a file name and returns a **list** of
   `Student` objects. It skips empty lines.
   Its annotation: `def load_students(path: str) -> list[Student]:`

3. Hold the loaded list in a variable called `students`.

4. Build a dictionary called `by_city`: the city as the key and a list of the
   names of the **passing** students in that city as the value. Keep the order
   from the file.

5. Hold the **name** of the student with the highest grade in a variable
   called `best`.

6. Print these in order: the number of students, `by_city`, and `best`.

**Expected output:**

```
5
{'London': ['Ada', 'Alan'], 'NewYork': ['Grace', 'Edith']}
Edith
```

> When adding to a list under a key that is not in the dictionary yet, you
> have to put an empty list there first:
> `if city not in by_city: by_city[city] = []`
