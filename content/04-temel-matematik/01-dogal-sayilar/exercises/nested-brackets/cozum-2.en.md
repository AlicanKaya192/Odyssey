**Idea:** Think of the expression as a tree: the outer operation is $100 - [\;\dots\;]$, and inside the square bracket is the sum of two pieces. Find each piece separately, then combine upwards.

**Step 1 — The two pieces of the square bracket.** Inside, there is one $+$ outside the round bracket:

$$
\underbrace{4 \cdot (15 - 3 \cdot 4)}_{\text{A}} \; + \; \underbrace{2^3}_{\text{B}}
$$

**Step 2 — Piece A.** First its bracket: $15 - 12 = 3$. Then $4 \cdot 3 = 12$. So $A = 12$.

**Step 3 — Piece B.** $2^3 = 2 \cdot 2 \cdot 2 = 8$.

**Step 4 — The square bracket.** $A + B = 12 + 8 = 20$.

**Step 5 — The outermost operation.** $100 - 20 = 80$.

**Check:** A rough check: the inside of the square bracket must be positive and less than $100$ (since $4 \cdot 3$ and $8$ are small); the result is between $0$ and $100$. $80$ is reasonable.

**Why the same result?** We did the same operations, just giving each piece a name and writing it separately. In long expressions, naming the pieces keeps you from mixing up which operation belongs where.

**Answer:** $80$.
