`nearest_distances(points, name)` should return, for each given fish, the
distance to its nearest neighbour among the real fish of species `name`.
Before the distance, divide length and weight by the species' standard
deviation (`part.std(axis=0)`). The result is a list rounded to 3 places. For
a real fish itself the distance must be 0.

**Expected output:**

```
[0.0, 0.012, 1.657]
```
