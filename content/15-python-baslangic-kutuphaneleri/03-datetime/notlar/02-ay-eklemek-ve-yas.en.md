`timedelta` counts days; it does not count months or years. Two common
calendar jobs need small functions.

## Adding months

What should happen when one month is added to 31 January? There is no 31
February; the common rule is to fall back to the last day of the month.
`calendar.monthrange(year, month)` gives how many days a month has (the
second value).

```python
import calendar
from datetime import date


def add_months(d, n):
    month_index = d.month - 1 + n
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    last = calendar.monthrange(year, month)[1]
    return date(year, month, min(d.day, last))


print(add_months(date(2026, 1, 31), 1))
print(add_months(date(2028, 1, 31), 1))
print(add_months(date(2026, 11, 15), 3))
print(add_months(date(2026, 3, 31), -1))
print(calendar.isleap(2026), calendar.isleap(2028))
print(calendar.monthrange(2026, 2)[1])
```

```text
2026-02-28
2028-02-29
2027-02-15
2026-02-28
False True
28
```

- Counting months from 0 (`month_index`), the year overflow is found with
  `// 12` and the new month with `% 12`; a negative `n` works too (one month
  back from March is February).
- 2028 is a leap year: 31 January + 1 month = 29 February.
- 15 November + 3 months is 15 February of the next year.

## Calculating an age

```python
from datetime import date


def age(birth, today):
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years


print(age(date(2000, 5, 20), date(2026, 5, 19)))
print(age(date(2000, 5, 20), date(2026, 5, 20)))
print((date(2026, 5, 19) - date(2000, 5, 20)).days // 365)
print((date(2026, 5, 19) - date(2000, 5, 20)).days / 365.25)
```

```text
25
26
26
25.9958932238193
```

One day before the birthday the person is 25, on the birthday 26. Whether one
must be subtracted from the year difference is decided by comparing the
`(month, day)` tuples: tuples compare by the first element first, and by the
second if those are equal.

Dividing the day difference by 365 gave a **wrong** result (26): the extra
days of the leap years in between add up and move it one day ahead. Dividing
by 365.25 does not give a whole number either. In calendar arithmetic, instead
of dividing days, compute with the calendar's own parts (year, month, day).
