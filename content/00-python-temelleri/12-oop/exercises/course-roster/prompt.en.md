In real programs classes do not stand alone; one holds another. In this
exercise you will write **two classes**.

**What you need to do:**

1. The `Student` class:
   - Its constructor takes `name` and `grade`.
   - The `is_passing` method returns `True` when the grade is **50 or more**.

2. The `Course` class:
   - Its constructor takes `title` and creates an **empty** `students` list.
   - The `enrol` method takes a `Student` object, adds it to the list and
     returns the **number of people** in the list.
   - The `passing_names` method returns the **names** of the students who
     passed, as a list.

3. Build a `Course` (`"Python"`) and enrol three students:
   `Ada` 90, `Brian` 40, `Grace` 75.
4. Print the number of students and then the passing names.

**Expected output:**

```
3
['Ada', 'Grace']
```

Note: the `students` list must be created **inside `__init__`**. If you write
it at class level, every course shares the same list.

> You can call a method on each student in the list:
> `if student.is_passing():`
