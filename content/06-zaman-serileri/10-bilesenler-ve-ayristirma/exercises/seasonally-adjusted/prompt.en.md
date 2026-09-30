Seasonally adjust the passenger series and compare the end of summer 2024
in its raw and adjusted forms.

**What to do:**

1. Do the multiplicative decomposition (`period=12`).
2. Compute the adjusted series: `adjusted = p / mul.seasonal`.
3. Print the raw values for June–September 2024 as a list.
4. Print the adjusted values for the same months, rounded to one decimal, as a
   list.
5. Compute the percentage change of September 2024 on the previous month for
   the raw and the adjusted series (`pct_change() * 100`, one decimal) and
   print them on one line.
6. Print the standard deviation of the monthly percentage change for the raw
   and the adjusted series, rounded to one decimal, on one line.

**Expected output:**

```
[432, 487, 480, 430]
[385.8, 393.3, 382.6, 408.2]
-10.4 6.7
9.6 2.2
```

The raw series shows a 10% fall in September, the adjusted one a rise: the
September drop happens every year, and this year it was smaller than expected.
The last line says the same for the whole series: most of the month-to-month
movement comes from the season; once adjusted, a far calmer series remains.
