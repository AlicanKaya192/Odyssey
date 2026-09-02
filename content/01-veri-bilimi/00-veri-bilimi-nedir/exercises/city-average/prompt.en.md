This is the ten-line example from the lesson. Once you have written it by
hand, `groupby` will never look like magic again.

**What you need to do:**

1. The `records` list is ready in the starter code.
2. Compute the **average** score for each city and keep the result in a
   dictionary called `averages`. The key is the city name, the value is the
   average.
3. Go through the cities in **alphabetical order** and print the city name
   and its average on each line.

**Expected output:**

```
Ankara 83.0
Bursa 88.0
Izmir 71.0
```

**Hint:** two dictionaries is the easiest way — one for totals, one as a
counter.

In pandas this will be one line: `data.groupby("city")["score"].mean()`
