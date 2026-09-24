**What is asked?** The model predicts a price for each house: it multiplies every feature by its weight, adds them up, and adds the constant $b$ at the end. We do this for all three houses.

**Idea:** Each component of $X\mathbf{w}$ is the dot product of one row of $X$ with $\mathbf{w}$ (the row view). Every row of $X$ is a house, so every dot product is one house's prediction. What the weights mean:

- Area: $+100$ thousand per hundred square metres.
- Rooms: $+20$ thousand per room.
- Age: $-2$ thousand per year (older houses are cheaper).

**Step 1 — House 1** (row 1: $1.2$, $3$, $10$). Multiply each feature by its weight, add, then add $10$:

$$
\begin{aligned}
\hat{y}_1 &= 1.2 \cdot 100 + 3 \cdot 20 + 10 \cdot (-2) + 10 \\
&= 120 + 60 - 20 + 10 \\
&= 170
\end{aligned}
$$

**Step 2 — House 2** (row 2: $0.8$, $2$, $25$):

$$
\begin{aligned}
\hat{y}_2 &= 0.8 \cdot 100 + 2 \cdot 20 + 25 \cdot (-2) + 10 \\
&= 80 + 40 - 50 + 10 \\
&= 80
\end{aligned}
$$

**Step 3 — House 3** (row 3: $1.5$, $4$, $5$):

$$
\begin{aligned}
\hat{y}_3 &= 1.5 \cdot 100 + 4 \cdot 20 + 5 \cdot (-2) + 10 \\
&= 150 + 80 - 10 + 10 \\
&= 230
\end{aligned}
$$

**Reading the result:** House 3 is the most expensive (largest, most rooms, newest). House 2 is the cheapest: small and 25 years old.

**Watch out:** $b$ is added to every prediction separately, not just to one.

**Answer:** $170$, $80$, $230$.
