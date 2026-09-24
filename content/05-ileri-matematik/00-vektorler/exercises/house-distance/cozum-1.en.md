**What is asked?** Each house is a point described by three numbers. We compute the straight-line distance between the two points twice: once with square metres, once with hundreds of square metres. The goal is to see how the unit changes the distance.

**Idea:** Euclidean distance works in three dimensions just as in two: find the difference vector, add up the squared components, take the square root. More components do not change the formula; the sum just gets one more term.

**Step 1 — The difference vector (square metres).** Subtract matching components:

$$
\begin{aligned}
\mathbf{a} - \mathbf{b} &= (120 - 100,\ 3 - 4,\ 10 - 12) \\
&= (20,\ -1,\ -2)
\end{aligned}
$$

Read it as: 20 m² apart, 1 room apart, 2 years apart.

**Step 2 — The length.**

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{20^2 + (-1)^2 + (-2)^2} \\
&= \sqrt{400 + 1 + 4} \\
&= \sqrt{405} \approx 20.12
\end{aligned}
$$

**Step 3 — Change the unit.** Dividing the area by 100 turns the houses into $\mathbf{a}' = (1.20,\ 3,\ 10)$ and $\mathbf{b}' = (1.00,\ 4,\ 12)$. Rooms and age stay the same:

$$
\mathbf{a}' - \mathbf{b}' = (0.20,\ -1,\ -2)
$$

**Step 4 — The new length.**

$$
\begin{aligned}
\|\mathbf{a}' - \mathbf{b}'\| &= \sqrt{0.20^2 + (-1)^2 + (-2)^2} \\
&= \sqrt{0.04 + 1 + 4} \\
&= \sqrt{5.04} \approx 2.24
\end{aligned}
$$

**Reading the result:** In the first calculation, $400$ of the $405$ under the square root came from the area; the room and age differences barely counted. After changing the unit the same two houses came about 9 times "closer", and this time rooms and age decided the distance. **The houses did not change, only the unit did.** A feature measured with large numbers dominates the distance.

**Where will you see this?** Methods that use distance (nearest neighbours, clustering) bring the features to the same scale first for exactly this reason.

**Answer:** $20.12$ and $2.24$.
