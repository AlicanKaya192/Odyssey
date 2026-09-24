**What is asked?** The sizes of the intersection and union of the complements.

**Idea:** Working with complements directly is awkward; De Morgan's laws turn them into a single complement. The size of a set's complement is $50$ minus the size of the set.

**Step 1 — The union.** $n(A \cup B) = 20 + 25 - 10 = 35$.

**Step 2 — $A' \cap B'$.** De Morgan: $A' \cap B' = (A \cup B)'$:

$$
n(A' \cap B') = 50 - 35 = 15
$$

**Step 3 — $A' \cup B'$.** De Morgan: $A' \cup B' = (A \cap B)'$:

$$
n(A' \cup B') = 50 - 10 = 40
$$

**Reading the result:** $A' \cap B'$ is "those in neither" ($15$); $A' \cup B'$ is "those not in both", that is, everyone outside the intersection ($40$).

**Watch out:** Working out $n(A' \cup B')$ as $n(A') + n(B') = 30 + 25 = 55$ counts the common ones twice; $55$ is even more than $50$.

**Answer:** $15$ and $40$.
