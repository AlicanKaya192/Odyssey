**What is asked?** The average code length under the right and the wrong assumption, and the difference.

**Idea:** $H(P) = -\sum p\log_2 p$, $H(P, Q) = -\sum p\log_2 q$, $D_{\mathrm{KL}} = H(P, Q) - H(P)$.

**Step 1 — $H(P)$.** $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{8} \cdot 3 + \frac{1}{8} \cdot 3 = 1.75$.

**Step 2 — $H(P, Q)$.** Every $q = \frac{1}{4}$: $-\sum p \cdot (-2) = 2$.

**Step 3 — KL.** $2 - 1.75 = 0.25$ bits.

**Check:** Directly: $\sum p\log_2\frac{p}{q} = \frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 0 + \frac{1}{8} \cdot (-1) + \frac{1}{8} \cdot (-1) = 0.25$ ✓.

**Watch out:** In cross-entropy the weights come from the true distribution $P$ and the inside of the log from the assumed $Q$; swapping them gives a different number.

**Answer:** $1.75$, $2$, $0.25$.
