Produce four different calendars with `pd.date_range`. This exercise
has no file.

**What to do:**

1. Produce the business days (`freq="B"`) of March 2024 and print how many
   there are.
2. Produce the month ends (`freq="ME"`) of the first six months of 2024 and
   print them as a list in `"%m-%d"` form.
3. Produce 4 shift starts 8 hours apart beginning at 06:00 on 9 March 2024
   (`periods=4`, `freq="8h"`) and print them as a list in `"%d %H:%M"` form.
4. Produce the Mondays (`freq="W-MON"`) of March 2024; print how many there
   are and the first one (`"%Y-%m-%d"`) on one line.

**Expected output:**

```
21
['01-31', '02-29', '03-31', '04-30', '05-31', '06-30']
['09 06:00', '09 14:00', '09 22:00', '10 06:00']
4 2024-03-04
```

In the second line February is `02-29`: `date_range` knows the leap year. In
the third line the last shift rolled into the next day. Had you written `"M"`
for month end you would have got an error; in current pandas it is `"ME"`.
