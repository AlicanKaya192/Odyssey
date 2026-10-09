**Estimating** a value with random numbers is called the Monte Carlo method.
The classic example is π: throw random points into a square of side 1 and
count those that land inside the quarter circle (radius 1). The quarter
circle's area is π/4 and the square's is 1; the share of points inside
approaches π/4.

```python
import math
import random


def estimate_pi(n, seed=0):
    r = random.Random(seed)
    inside = 0
    for _ in range(n):
        x, y = r.random(), r.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / n


for n in (100, 1000, 10000, 100000, 1000000):
    estimate = estimate_pi(n)
    print(n, estimate, round(abs(estimate - math.pi), 4))
```

```text
100 3.04 0.1016
1000 3.128 0.0136
10000 3.1352 0.0064
100000 3.14844 0.0068
1000000 3.14244 0.0008
```

With 100 points the estimate is 3.04 (error 0.10); with a million points
3.14244 (error 0.0008). The error usually shrinks as slowly as the square root
of the number of points: 100 times the points, about 10 times less error. The
table also shows that this is bumpy: going from 10,000 to 100,000 points the
error grew a little, because every estimate depends on luck.

Monte Carlo helps with questions whose formula is unknown or hard to solve:
the chance of winning a game, how long a queue will get, the possible
outcomes of an investment. The Randomised Algorithms section of the Algorithm
Techniques module has more.
