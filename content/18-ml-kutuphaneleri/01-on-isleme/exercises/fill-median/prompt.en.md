`fill_median(rows)` should fill the missing values (`None`) in the number table
**with the median** and add a "was missing" column for each column with gaps
(`SimpleImputer(strategy="median", add_indicator=True)`). Return the result
as a list of lists rounded to 2 places. The starter code fills with the mean
and adds no flag.

**Expected output:**

```
[1.0, 7.0, 0.0, 0.0]
[3.0, 8.0, 1.0, 0.0]
[3.0, 8.0, 0.0, 1.0]
[100.0, 9.0, 0.0, 0.0]
```
