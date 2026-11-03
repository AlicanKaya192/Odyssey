`assign_cities(user_cities, seed=0)` should take each user's city, assign
half of the cities to B and return the B cities as a sorted list. The
starter code assigns users one by one: a city gets split into two groups.
Sort the cities (`sorted(set(...))`), shuffle (`rng.permutation`) and take
the first half.

**Expected output:**

```text
['W', 'Y']
```
