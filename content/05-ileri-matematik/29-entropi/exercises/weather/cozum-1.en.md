**What is asked?** The entropy of a distribution, a unit conversion and the upper bound.

**Idea:** $H = \sum p \cdot (-\log_2 p)$.

**Step 1 — Bits.** $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{4} \cdot 2 = 1.5$ bits.

**Step 2 — Nats.** $1.5 \cdot 0.6931 \approx 1.040$ nats.

**Step 3 — Upper bound.** $\log_2 3 \approx 1.585$ bits.

**Check:** $1.5 < 1.585$: the distribution is not uniform, so its entropy is below the bound ✓.

**Watch out:** Converting to nats multiplies by $\ln 2$; dividing gives a wrong number like $2.164$.

**Answer:** $1.5$, $\approx 1.040$, $\approx 1.585$.
