**What is asked?** The MLE of an event never seen, and corrected estimates.

**Idea:** MLE $\frac{k}{n}$; Laplace $\frac{k + 1}{n + 2}$.

**Step 1 — MLE.** $\frac{0}{40} = 0$.

**Step 2 — Spam, Laplace.** $\frac{0 + 1}{40 + 2} = \frac{1}{42} \approx 0.0238$.

**Step 3 — Normal, Laplace.** $\frac{12 + 1}{60 + 2} = \frac{13}{62} \approx 0.210$. (The MLE was $0.2$; with plenty of data the correction changes little.)

**Check:** With the MLE, an email containing "invoice" gets a spam likelihood of $0$; however spam-like every other word is, the result is "normal". With the corrected estimate the likelihood ratio is $\frac{0.210}{0.0238} \approx 8.8$: strong but not absolute evidence ✓.

**Watch out:** The Laplace correction has a large effect with little data and a small one with a lot; the spam estimate moves from $0$ to $0.024$, the normal one only from $0.2$ to $0.21$.

**Answer:** $0$, $\approx 0.0238$, $\approx 0.210$.
