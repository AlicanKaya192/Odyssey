When you get a new time series, ask these questions in order before touching
a model. The code for each comes in later sections; here what matters is
**what** you look at.

## First look checklist

1. **What is the frequency?** Hourly, daily, monthly? Mixed?
2. **Where does it start and end?** How many observations, how many years?
3. **Are timestamps missing?** If there should be one row per day, are there
   1096 rows for 1096 days?
4. **Are timestamps repeated?** Did two rows land on the same day?
5. **What does the value measure?** Is it a **total** (the day's sales) or a
   **point-in-time value** (the evening closing price, the temperature right
   now)? When you turn them into weekly figures you add up the first, and
   take the mean or the last value of the second.
6. **Plot it.** The whole series, then a narrow window such as one month.
7. **Is there a trend?** Look at the averages year by year.
8. **Is there seasonality, and how long is it?** Day of week, month, hour of
   day.
9. **Is there a break?** Did the level of the series shift for good at some
   point?
10. **What is the time zone?** Especially for hourly data: UTC or local time?
11. **What is the split plan?** Train up to which date, test from which date?

## Common mistakes

| Mistake | Why it is wrong |
|---|---|
| Shuffling the rows (`sample(frac=1)`, `shuffle=True`) | The order is the data; shuffling loses the information |
| A random split (`train_test_split`) | The future ends up in training and the past in testing; the score is unreal |
| Leaving dates as text | Date operations do not work; day-first dates sort wrongly |
| Not noticing missing days | "The previous row" is no longer "yesterday" |
| Mistaking a cycle for seasonality | Modelling a repeat that is not tied to the calendar with a fixed length |
| Aggregating totals and point values the same way | Adding up a price to get a weekly figure gives a meaningless number |
| Modelling before plotting | Missing the break, the outlier, the gap |

## What is not a time series

Not every table with a date column is a time series. A customer table having
a `signup_date` column does not make it one: the rows are still different
customers. The question is: **are the rows measurements of the same thing
over time?** If yes, it is a time series.
