**What is asked?** How many of a good model's alarms are correct for a rare class.

**Idea:** Turn the rates into transaction counts; precision is the share of real alarms among all alarms.

**Step 1 — The groups.** Fraud $100{,}000 \cdot 0.002 = 200$; normal $99{,}800$.

**Step 2 — The alarms.** Real: $200 \cdot 0.95 = 190$. False: $99{,}800 \cdot 0.01 = 998$. Total $1188$.

**Step 3 — Precision.** $\frac{190}{1188} \approx 0.160$.

**Check:** With Bayes' rule $\frac{0.95 \cdot 0.002}{0.95 \cdot 0.002 + 0.01 \cdot 0.998} \approx 0.160$ ✓.

**Watch out:** "Catches $95$ percent, $99$ percent correct" does not mean most alarms are right; $5$ of every $6$ alarms are false. Accuracy misleads too: the model classifies $190 + 98{,}802 = 98{,}992$ of $100{,}000$ transactions correctly, about $99$ percent.

**Answer:** $1188$, $190$, $\approx 0.160$.
