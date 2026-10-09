Write the function `letter_grades(scores)`: turn each score into a letter
grade: below 60 `F`, 60–69 `D`, 70–79 `C`, 80–89 `B`, 90 and above `A`. The
boundaries are in the list `[60, 70, 80, 90]`, the letters in the string
`"FDCBA"`; `bisect.bisect(boundaries, score)` gives the letter's index.

**Expected output:**

```
['F', 'A', 'C', 'C', 'B', 'D', 'F']
```
