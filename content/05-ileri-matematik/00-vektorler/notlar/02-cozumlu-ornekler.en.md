A worked example, step by step, for each method in the lesson. Try the question yourself first, then read the solution.

## 1. A vector from two points and its reverse

**Question:** For $A(-2, 5)$ and $B(3, -1)$, what are $\overrightarrow{AB}$ and $\overrightarrow{BA}$?

End minus start:

$$
\overrightarrow{AB} = B - A = \big(3 - (-2),\ -1 - 5\big) = (5,\ -6)
$$

$$
\overrightarrow{BA} = A - B = (-2 - 3,\ 5 - (-1)) = (-5,\ 6)
$$

Each is the negative of the other: same length, opposite direction. Watch
the sign when subtracting a negative number: $3 - (-2) = 5$.

## 2. A linear combination in three dimensions

**Question:** What is $3\,(2, -1, 0) - 2\,(1, 1, 4)$?

First multiply each vector by its scalar, then subtract component by component:

$$
(6, -3, 0) - (2, 2, 8) = (6 - 2,\ -3 - 2,\ 0 - 8) = (4,\ -5,\ -8)
$$

The method is the same whatever the dimension.

## 3. Finding a missing coefficient

**Question:** If $a\,(2, 1) + b\,(-1, 3) = (0, 7)$, what are $a$ and $b$?

Expand the left side into components:

$$
(2a - b,\ a + 3b) = (0,\ 7)
$$

If two vectors are equal, their components are equal one by one. Two
equations follow:

$$
2a - b = 0 \qquad a + 3b = 7
$$

From the first, $b = 2a$. Substitute into the second: $a + 6a = 7$, so
$a = 1$ and $b = 2$.

**Check:** $1\,(2, 1) + 2\,(-1, 3) = (2, 1) + (-2, 6) = (0, 7)$. ✓

Writing a vector as a linear combination of other vectors always means
solving a **system of equations**. The Linear Systems chapter of the Advanced Mathematics module
does this on a large scale.

## 4. Length and unit vector

**Question:** For $\mathbf{v} = (5, -12)$, what are $\|\mathbf{v}\|$ and the unit vector?

$$
\|\mathbf{v}\| = \sqrt{5^2 + (-12)^2} = \sqrt{25 + 144} = \sqrt{169} = 13
$$

$$
\hat{\mathbf{v}} = \left(\frac{5}{13},\ \frac{-12}{13}\right) \approx (0.385,\ -0.923)
$$

$(5, 12, 13)$ is a Pythagorean triple; the minus sign does not change the length.

## 5. Midpoint and mean vector

**Question:** What is the point exactly halfway between $A(1, 1)$ and $B(5, 7)$?

The midpoint is the average of the two vectors:

$$
M = \frac{A + B}{2} = \frac{(6, 8)}{2} = (3, 4)
$$

The same idea works for many points. If three people's (height, weight)
vectors are $(160, 55)$, $(170, 65)$ and $(180, 75)$, the mean vector is:

$$
\frac{(160, 55) + (170, 65) + (180, 75)}{3} = \frac{(510, 195)}{3} = (170,\ 65)
$$

Clustering algorithms (k-means) find the centre of each cluster in exactly
this way.

## 6. A point on a line

**Question:** What is the point one third of the way from $A(2, 1)$ to $B(8, 10)$?

Start at $A$ and walk one third of $\overrightarrow{AB}$:

$$
\overrightarrow{AB} = (6, 9) \qquad
A + \tfrac{1}{3}\,\overrightarrow{AB} = (2, 1) + (2, 3) = (4,\ 4)
$$

The general form is $A + t\,\overrightarrow{AB}$: $t = 0$ gives $A$,
$t = 1$ gives $B$, and every $t$ in between is a point on the segment.

## 7. Nearest neighbour

**Question:** Which is closer to $P(2, 3)$: $Q(5, 7)$ or $R(7, 1)$?

$$
\|Q - P\| = \|(3, 4)\| = 5
\qquad
\|R - P\| = \|(5, -2)\| = \sqrt{25 + 4} = \sqrt{29} \approx 5.39
$$

$Q$ is closer. You could also compare without square roots: $25 < 29$.
Comparing squared lengths gives the same answer and needs no calculator.
