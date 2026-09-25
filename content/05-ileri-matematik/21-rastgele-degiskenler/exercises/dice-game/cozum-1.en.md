**What is asked?** An event's probability, a game's expected gain, and the loss that makes the game fair.

**Idea:** The net gain is a random variable: $30$, $60$ or $-8$. The expected value is the sum of each gain weighted by its probability.

**Step 1 — Probabilities.** $P(7) = \frac{6}{36} = \frac{1}{6}$; $P(2 \text{ or } 12) = \frac{2}{36}$; the rest $\frac{28}{36}$.

**Step 2 — Expected gain.**

$$
\begin{aligned}
E &= 30 \cdot \tfrac{6}{36} + 60 \cdot \tfrac{2}{36} - 8 \cdot \tfrac{28}{36} \\
&= \frac{180 + 120 - 224}{36} = \frac{76}{36} = \frac{19}{9} \approx 2.11
\end{aligned}
$$

**Step 3 — The fair loss.** $\frac{180 + 120 - 28L}{36} = 0$, $L = \frac{300}{28} = \frac{75}{7} \approx 10.71$.

**Check:** With $L = 8$ the expected gain is positive, in the player's favour; to be fair the loss has to grow ✓.

**Watch out:** Treating the three outcomes as equally likely and taking $\frac{30 + 60 - 8}{3}$; the probabilities differ greatly.

**Answer:** $\frac{1}{6}$, $\frac{19}{9} \approx 2.11$, $\frac{75}{7} \approx 10.71$.
