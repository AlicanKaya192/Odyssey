An order was placed on 27 February 2024 and delivered on 4 March 2024.

**What to do:**

1. Build the two dates as `date` objects.
2. Print the number of days between them (`(delivery - order).days`).
3. Print the name of the delivery day (`strftime("%A")`).
4. Build the same two days for the year 2023 and print the number of days
   between them.

**Expected output:**

```
6
Monday
5
```

The same two dates give different results in two years: 2024 is a leap year
and 29 February sits in between. It is the easiest thing to miss when
counting by hand.
