**What is asked?** When two different cycles line up, and how many times they do so within a given time.

**Idea:** Line A leaves at minutes $0, 12, 24, 36, \dots$; line B at $0, 18, 36, \dots$ Joint departures are the **common multiples** of the two. The first is the LCM; the rest are multiples of the LCM.

**Step 1 — Prime factors.**

$$
12 = 2^2 \cdot 3, \qquad 18 = 2 \cdot 3^2
$$

**Step 2 — LCM: all primes, larger exponents.**

$$
\text{LCM}(12, 18) = 2^2 \cdot 3^2 = 36
$$

They leave together again $36$ minutes after the first joint departure, that is, at $08{:}36$.

**Step 3 — The time span.** From $08{:}00$ to $12{:}00$ is $4 \cdot 60 = 240$ minutes.

**Step 4 — Count the multiples of $36$.** Joint departures are at minutes $0, 36, 72, 108, 144, 180, 216$. The next, $252 > 240$, is after $12{:}00$. With division with remainder: $240 = 36 \cdot 6 + 24$; $6$ multiples plus the start ($0$):

$$
6 + 1 = 7
$$

**Watch out:** Saying $240 \div 36 \approx 6$ and writing $6$ is a common slip; the first departure at $08{:}00$ counts too.

**Answer:** $36$ minutes; $7$ times.
