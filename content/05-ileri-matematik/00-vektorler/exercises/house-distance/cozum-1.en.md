**1. In square metres:**

$$
\mathbf{a} - \mathbf{b} = (20,\ -1,\ -2)
$$

$$
\|\mathbf{a} - \mathbf{b}\| = \sqrt{20^2 + (-1)^2 + (-2)^2} = \sqrt{400 + 1 + 4} = \sqrt{405} \approx 20.12
$$

**2. In hundreds of square metres:**

$$
\mathbf{a}' - \mathbf{b}' = (0.20,\ -1,\ -2)
$$

$$
\sqrt{0.04 + 1 + 4} = \sqrt{5.04} \approx 2.24
$$

**What happened?** In the first calculation almost all of the distance came from the area ($400$ of the $405$). Changing the unit made the distance between the same two houses $9$ times smaller, and this time the room and age differences were decisive. **The houses did not change, only the unit did.**

That is why methods that use distance (nearest neighbours, clustering) first bring the features to the same scale.

**Answer: $20.12$ and $2.24$**
