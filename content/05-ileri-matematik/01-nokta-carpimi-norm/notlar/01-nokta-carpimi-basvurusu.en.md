The short version of everything in the lesson. Come back here when a question stops you.

## Definitions

| Concept | Formula |
|---|---|
| Dot product | $\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + \cdots + a_n b_n$ |
| Geometric form | $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta$ |
| Length | $\|\mathbf{a}\| = \sqrt{\mathbf{a} \cdot \mathbf{a}}$ |
| Angle | $\cos\theta = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$ |
| Scalar projection | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|}$ |
| Vector projection | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}$ |
| Cosine similarity | $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$, between $-1$ and $1$ |

## Properties

- $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$
- $\mathbf{a} \cdot (\mathbf{b} + \mathbf{c}) = \mathbf{a} \cdot \mathbf{b} + \mathbf{a} \cdot \mathbf{c}$
- $(k\,\mathbf{a}) \cdot \mathbf{b} = k\,(\mathbf{a} \cdot \mathbf{b})$
- $\mathbf{a} \cdot \mathbf{a} = \|\mathbf{a}\|^2 \ge 0$
- Cauchy–Schwarz: $|\mathbf{a} \cdot \mathbf{b}| \le \|\mathbf{a}\|\,\|\mathbf{b}\|$
- $\|\mathbf{a} + \mathbf{b}\|^2 = \|\mathbf{a}\|^2 + 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2$

The last line turns into Pythagoras' theorem when $\mathbf{a} \cdot \mathbf{b} = 0$.

## Sign table

| $\mathbf{a} \cdot \mathbf{b}$ | Angle | Meaning |
|---|---|---|
| $> 0$ | $0° \le \theta < 90°$ | roughly the same way |
| $= 0$ | $\theta = 90°$ | perpendicular |
| $< 0$ | $90° < \theta \le 180°$ | roughly opposite ways |

## Cosine values

| $\theta$ | $0°$ | $30°$ | $45°$ | $60°$ | $90°$ | $120°$ | $135°$ | $180°$ |
|---|---|---|---|---|---|---|---|---|
| $\cos\theta$ | $1$ | $\approx 0.866$ | $\approx 0.707$ | $0.5$ | $0$ | $-0.5$ | $\approx -0.707$ | $-1$ |

## Norms

| Norm | Formula | $(3, -4)$ |
|---|---|---|
| $L_1$ (Manhattan) | $\sum \lvert a_i \rvert$ | $7$ |
| $L_2$ (Euclidean) | $\sqrt{\sum a_i^2}$ | $5$ |
| $L_\infty$ | $\max \lvert a_i \rvert$ | $4$ |

Always $L_\infty \le L_2 \le L_1$.

## Practical tips

- A vector perpendicular to $(p, q)$ in the plane: $(-q, p)$.
- If two vectors point the same way, their cosine similarity is $1$; one is a positive multiple of the other.
- Between unit vectors, cosine similarity = plain dot product.
- A vector's $x$ component is its projection onto $(1, 0)$.
