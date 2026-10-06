The student lists of two courses are given as **sets**:

```python
class_a = {"Ada", "Alan", "Grace", "Linus", "Guido"}
class_b = {"Grace", "Guido", "Margaret", "Linus", "Dennis", "Ken"}
```

Find:

- `both`: the students who attend both courses
- `only_a`: those who attend course A only
- `only_b`: those who attend course B only
- `total`: the number of **different** students who attend at least one
  course

```
Both: ['Grace', 'Guido', 'Linus']
Only A: ['Ada', 'Alan']
Only B: ['Dennis', 'Ken', 'Margaret']
Total: 8
```

Set operations bring this down to single lines: intersection `&`,
difference `-`, union `|`. Think on paper first about what each one
gives: are `class_a - class_b` and `class_b - class_a` the same thing?

> Watch out: a set's items may not print in the same order on every run.
> So when you print, turn it into a sorted list with `sorted()`. For
> `total`, adding up the lengths of the two sets would count the students
> who attend both courses twice.
