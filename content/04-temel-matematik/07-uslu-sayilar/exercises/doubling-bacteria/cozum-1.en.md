**What is asked?** The value of an exponentially growing quantity after a given time, and the time to reach a given value.

**Idea:** A number that doubles $k$ times is multiplied by $2^k$. First turn the time into a number of doublings, then write $100 \cdot 2^k$.

**Step 1 — The number of doublings.** $2$ hours $= 120$ minutes; $120 \div 20 = 6$ doublings.

**Step 2 — After $2$ hours.**

$$
100 \cdot 2^6 = 100 \cdot 64 = 6\,400
$$

**Step 3 — The doublings needed for $51\,200$.** If $100 \cdot 2^k = 51\,200$, then

$$
2^k = 512 = 2^9 \quad\Rightarrow\quad k = 9
$$

**Step 4 — The time.** $9$ doublings $\cdot\, 20$ minutes $= 180$ minutes ($3$ hours).

**Check:** $100 \to 200 \to 400 \to 800 \to 1\,600 \to 3\,200 \to 6\,400$ (6 steps) $\to 12\,800 \to 25\,600 \to 51\,200$ (9 steps) ✓.

**Watch out:** Writing "$\cdot 6$" or "$+ 6 \cdot 100$" for $2$ hours treats doubling as addition. Each doubling multiplies the previous number by two.

**Answer:** $6\,400$ bacteria; $180$ minutes.
