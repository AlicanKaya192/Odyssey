**What is asked?** Softmax and sigmoid probabilities from the same scores, and how a probability changes when a class is added.

**Idea:** Softmax divides each class's $e^{z}$ by the total. For the sigmoid, $e^{-(z_1 - z_2)}$ is found from the given numbers with the exponent rules.

**Step 1 — Two-class softmax.**

$$
p_1 = \frac{12}{12 + 4} = \frac{12}{16} = \frac{3}{4}
$$

**Step 2 — Sigmoid.** $e^{-(z_1 - z_2)} = e^{z_2 - z_1} = \frac{e^{z_2}}{e^{z_1}} = \frac{4}{12} = \frac{1}{3}$.

$$
\sigma(z_1 - z_2) = \frac{1}{1 + \frac{1}{3}} = \frac{1}{\frac{4}{3}} = \frac{3}{4}
$$

**Step 3 — Three classes.**

$$
p_1 = \frac{12}{12 + 4 + 4} = \frac{12}{20} = \frac{3}{5}
$$

**Check:** With three classes the probabilities are $\frac{12}{20}, \frac{4}{20}, \frac{4}{20}$; they add up to $1$ ✓.

**Watch out:** When a new class is added, the first class's probability drops even though its score did not change: softmax probabilities depend on each other, the denominator holds every class.

**Answer:** $\frac{3}{4}$, $\frac{3}{4}$, $\frac{3}{5}$.
