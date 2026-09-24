**What is asked?** The sizes of the union, intersection and difference of two sets.

**Idea:** With small sets the safest route is to write the operations out: union "in either", intersection "in both", difference "in $A$ but not in $B$".

**Step 1 — The intersection.** What is in both lists:

$$
A \cap B = \{4, 5, 6\}, \quad n = 3
$$

**Step 2 — The union.** Everything, without repeats:

$$
A \cup B = \{1, 2, 3, 4, 5, 6, 7, 8\}, \quad n = 8
$$

**Step 3 — The difference.** Remove the common ones from $A$:

$$
A \setminus B = \{1, 2, 3\}, \quad n = 3
$$

**Check:** $n(A \cup B) = 6 + 5 - 3 = 8$ ✓.

**Watch out:** Counting the union as $6 + 5 = 11$ counts the three common elements twice.

**Answer:** $8$, $3$, $3$.
