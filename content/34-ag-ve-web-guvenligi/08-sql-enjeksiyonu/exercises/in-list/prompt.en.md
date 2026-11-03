The `users` table is ready. `count_in(cities)` should return the
number of users whose city is one of the cities in the list. Make one `?`
per city (`", ".join("?" * len(cities))`) and give the values separately.
If the list is empty, return `0` without running a query. The starter code
pastes the cities into the text with quotes and breaks on `L'Aquila`.

**Expected output:**

```
2
3
0
0
```
