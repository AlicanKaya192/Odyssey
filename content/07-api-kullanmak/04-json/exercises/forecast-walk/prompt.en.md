`forecast.json` holds a four-day forecast. Each day is a dictionary, and
**not every day has wind information.**

**What to do:**

1. Read the file into a variable called `data` with `json.load`.
2. For every day, print the day's name, the temperature and the wind speed.
   If there is no wind, print `?` instead of the speed (use `get`).
3. Put the name of the hottest day into the variable `hottest` and print it.

**Expected output:**

```
mon 24 wind 12
tue 21 wind ?
wed 26 wind 7
thu 19 wind 20
hottest: wed
```
