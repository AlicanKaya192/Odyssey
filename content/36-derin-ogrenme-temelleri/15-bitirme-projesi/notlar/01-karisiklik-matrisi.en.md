A **row** of the confusion matrix shows where the real examples of that digit
went; a **column** shows where the examples the model called that digit came
from:

```python
print("3:", matrix[3].tolist())
print("8:", matrix[8].tolist())
print("col 8:", matrix[:, 8].tolist())
for digit in range(10):
    row = matrix[digit]
    if row[digit] < row.sum():
        print(digit, round(100 * row[digit].item() / row.sum().item(), 1))
```

```text
3: [0, 0, 1, 31, 0, 0, 0, 0, 4, 0]
8: [0, 0, 0, 0, 0, 0, 0, 0, 38, 0]
col 8: [0, 2, 0, 4, 0, 0, 0, 0, 38, 0]
1 94.6
3 86.1
4 97.4
5 94.7
7 97.6
9 97.4
```

- Row 3: of 36 real 3s, 31 are right, 4 went to 8 and 1 to 2.
- Column 8: of the 44 images the model called "8", 4 were really 3s and 2
  were 1s.
- The last printout lists the per-class accuracy only for digits with
  errors. The lowest is 3, at 86.1%. If one class is clearly below the others,
  looking one by one at its wrongly predicted examples is a good next step.
- Note that per-class accuracy is divided by the row total: that is the
  class's **recall**.
