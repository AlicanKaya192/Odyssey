The whole module is in this exercise: you read a dirty file, clean it and
summarise it. You also report **how many records you started with and how
many you ended with**.

The whole file (`results_raw.csv`):

```text
id,city,score
1,Ankara,82
2,Izmir ,74
3,ankara,91
4,Bursa,
5,Izmir,68
5,Izmir,68
6,ANKARA,abc
7,bursa ,77
8,Adana,85
```

**What to do:**

1. Write the import, read the file as `raw` and take a copy.
2. Clean the `city` column: strip the spaces around it and capitalise it.
3. Turn `score` into numbers — anything that cannot be converted becomes
   empty.
4. Keep the number of rows you started with in a variable.
5. Drop records that repeat the same `id` and keep the remaining row count.
6. Count how many records have an empty score, then drop those rows.
7. Print the four numbers **side by side on one line**: start, unique,
   missing, remaining.
8. Print the number of records and the average (one decimal) per city as
   **two separate dictionaries**.

**Expected output:**

```
9 8 2 6
{'Adana': 1, 'Ankara': 2, 'Bursa': 1, 'Izmir': 2}
{'Adana': 85.0, 'Ankara': 86.5, 'Bursa': 77.0, 'Izmir': 71.0}
```

**Three things to watch:**

- **The order:** group before fixing the city and `Izmir ` and `Izmir`,
  `ankara` and `ANKARA` end up in separate groups.
- **`abc` is not an error; it is dirt from the data.** `errors="coerce"`
  turns it into an empty value and keeps the program going.
- **The numbers go into the report.** You started with nine rows and ended
  with six. An analysis that does not say so hides something the reader
  needs to know.

Look at the last dictionaries: **Bursa's average rests on a single
student** — one of its two records was empty. Adana has a single record
too. "Adana is second with 85" is technically true, but a ranking built on
one score is not reliable.
