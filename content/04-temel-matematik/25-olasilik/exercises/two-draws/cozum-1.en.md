**What is asked?** The probabilities of three events in two draws without replacement.

**Idea:** In the tree, multiply along a path and add the matching paths. The second draw's probabilities depend on the first.

**Step 1 — Both red.** $\frac{4}{10} \cdot \frac{3}{9} = \frac{12}{90} = \frac{2}{15}$.

**Step 2 — Different colours.** RB: $\frac{4}{10} \cdot \frac{6}{9} = \frac{24}{90}$. BR: $\frac{6}{10} \cdot \frac{4}{9} = \frac{24}{90}$. Total $\frac{48}{90} = \frac{8}{15}$.

**Step 3 — Second red.** RR and BR: $\frac{12}{90} + \frac{24}{90} = \frac{36}{90} = \frac{2}{5}$.

**Check:** Four paths: RR $12$, RB $24$, BR $24$, BB $\frac{6}{10} \cdot \frac{5}{9} = 30$; $12 + 24 + 24 + 30 = 90$ ✓.

**Watch out:** In the third question the first ball is unknown; the second draw's probability is therefore not a conditional probability but the sum of two paths.

**Answer:** $\frac{2}{15}$, $\frac{8}{15}$, $\frac{2}{5}$.
