**What is asked?** Writing $2\,025$ as $2\,025 = 17 \cdot q + r$, where $q$ is the quotient, $r$ the remainder and $0 \le r < 17$.

**Idea:** Wear the dividend down with big chunks that are easy to compute: first $100$ times $17$, then $10$ times, then small numbers. We add up how many $17$s we took off in each chunk.

**Step 1 — $100$ lots of $17$.** $17 \cdot 100 = 1\,700$. That leaves $2\,025 - 1\,700 = 325$.

**Step 2 — $10$ lots of $17$.** $17 \cdot 10 = 170$. That leaves $325 - 170 = 155$.

**Step 3 — How many $17$s in the remaining $155$?** $17 \cdot 9 = 153$. That leaves $155 - 153 = 2$.

**Step 4 — Add up.** The number of $17$s taken off is $100 + 10 + 9 = 119$; $2$ is left, and $2 < 17$.

**Check:**

$$
17 \cdot 119 + 2 = 2\,023 + 2 = 2\,025
$$

✓

**Watch out:** A result such as "quotient 118, remainder 19" is wrong: the remainder cannot exceed the divisor; take one more $17$ off $19$.

**Answer:** Quotient $119$, remainder $2$.
