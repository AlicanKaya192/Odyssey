Three students, three exams. You have the scores in a single row; you will
turn them into a table and compute in both directions.

The `flat` array is ordered student by student: the first three numbers are
the first student's three exams, the next three the second student's, and so
on.

**What you need to do:**

1. Turn `flat` into **3 rows and 3 columns** and call it `matrix`.
2. Compute each **student's** total score into an array called
   `per_student`.
3. Compute each **exam's** average into an array called `per_exam`.
4. Find the **position** of the student with the highest total and keep it in
   a variable called `best`.
5. Print, in order: `matrix`, `per_student`, `per_exam` rounded to two
   places, and `best`.

**Expected output:**

```
[[12 15  9]
 [20 18 11]
 [14 17 13]]
[36 49 44]
[15.33 16.67 11.  ]
1
```

**The real question:** which one is `axis=0` and which is `axis=1`? Since the
rows are students, a per-student total goes along the row. If you mix them up
the shape of the output will not match — that is the thing telling you.
