A worked example, step by step, for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Finding the value that makes vectors perpendicular

**Question:** $(2, k, 1)$ and $(3, -1, 4)$ are perpendicular. What is $k$?

If they are perpendicular, their dot product is zero:

$$
2 \cdot 3 + k \cdot (-1) + 1 \cdot 4 = 0 \;\Rightarrow\; 10 - k = 0 \;\Rightarrow\; k = 10
$$

No angle measuring needed, just one linear equation.

## 2. An acute angle

**Question:** What is the angle between $(1, 2)$ and $(3, 1)$ in degrees?

$$
\mathbf{a} \cdot \mathbf{b} = 3 + 2 = 5
\qquad
\|\mathbf{a}\| = \sqrt{5}
\qquad
\|\mathbf{b}\| = \sqrt{10}
$$

$$
\cos\theta = \frac{5}{\sqrt{5}\sqrt{10}} = \frac{5}{\sqrt{50}} = \frac{5}{5\sqrt{2}} = \frac{1}{\sqrt{2}}
\quad\Rightarrow\quad \theta = 45°
$$

A product of square roots can be written as a single square root:
$\sqrt{5}\sqrt{10} = \sqrt{50} = 5\sqrt{2}$.

## 3. An obtuse angle

**Question:** Is the angle between $(2, -1)$ and $(1, 3)$ greater than $90°$?

Look at the sign without computing the angle:

$$
(2, -1) \cdot (1, 3) = 2 - 3 = -1 < 0
$$

Negative, so the angle is greater than $90°$. If you want the exact value,
$\cos\theta = \frac{-1}{\sqrt{5}\sqrt{10}} \approx -0.141$ and
$\theta \approx 98.1°$.

## 4. Dot product from lengths and angle

**Question:** If $\|\mathbf{a}\| = 4$, $\|\mathbf{b}\| = 3$ and the angle between them is $60°$, what is $\mathbf{a} \cdot \mathbf{b}$?

$$
\mathbf{a} \cdot \mathbf{b} = 4 \cdot 3 \cdot \cos 60° = 12 \cdot 0.5 = 6
$$

The dot product can be computed without knowing the components.

## 5. Projection

**Question:** What is the projection of $\mathbf{a} = (4, 3)$ onto the direction of $\mathbf{b} = (1, 1)$?

$$
\mathbf{a} \cdot \mathbf{b} = 7 \qquad \mathbf{b} \cdot \mathbf{b} = 2
$$

Vector projection:

$$
\frac{7}{2}\,(1, 1) = (3.5,\ 3.5)
$$

Scalar projection (the length of the shadow): $\dfrac{7}{\sqrt{2}} \approx 4.95$.
Check: $\|(3.5, 3.5)\| = 3.5\sqrt{2} \approx 4.95$. ✓

## 6. Recommending with cosine similarity

**Question:** Users rated four films from 0 to 5. Is B or C more similar to A?

| | Film 1 | Film 2 | Film 3 | Film 4 |
|---|---|---|---|---|
| A | 5 | 3 | 0 | 1 |
| B | 4 | 0 | 0 | 1 |
| C | 0 | 1 | 5 | 4 |

$$
\cos(A, B) = \frac{20 + 0 + 0 + 1}{\sqrt{35}\,\sqrt{17}} = \frac{21}{\sqrt{595}} \approx 0.86
$$

$$
\cos(A, C) = \frac{0 + 3 + 0 + 4}{\sqrt{35}\,\sqrt{42}} = \frac{7}{\sqrt{1470}} \approx 0.18
$$

B is far more similar. Films B liked that A has not watched yet are the
first candidates to recommend to A.

## 7. Three norms

**Question:** What are the $L_1$, $L_2$ and $L_\infty$ norms of $(2, -6, 3)$?

$$
L_1 = 2 + 6 + 3 = 11
\qquad
L_2 = \sqrt{4 + 36 + 9} = \sqrt{49} = 7
\qquad
L_\infty = 6
$$

The order is always the same: $6 \le 7 \le 11$.
