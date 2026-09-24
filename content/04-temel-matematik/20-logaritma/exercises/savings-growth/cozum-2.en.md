**Idea:** The "divide by 1000 first" step in the first method is a shortcut. Without dividing, taking the logarithm of both sides straight away leads to the same place; this time the **product** and **quotient** rules come into play. This route shows how the rules work together.

**Step 1 — Take the logarithm of both sides.**

$$
\ln (1000 \cdot 1.08^t) = \ln 2500
$$

**Step 2 — Split the product on the left.** Product rule: $\ln (xy) = \ln x + \ln y$. Then the power rule brings the exponent down:

$$
\begin{aligned}
\ln 1000 + \ln (1.08^t) &= \ln 2500 \\
\ln 1000 + t \ln 1.08 &= \ln 2500
\end{aligned}
$$

**Step 3 — Isolate $t$.** Move $\ln 1000$ to the other side, then divide by $\ln 1.08$:

$$
t = \frac{\ln 2500 - \ln 1000}{\ln 1.08}
$$

**Step 4 — Simplify the numerator.** Quotient rule: $\ln x - \ln y = \ln \frac{x}{y}$.

$$
\ln 2500 - \ln 1000 = \ln \frac{2500}{1000} = \ln 2.5
$$

We reached the same formula as in the first method:

$$
t = \frac{\ln 2.5}{\ln 1.08} \approx 11.91
$$

**Why the same result?** The division of the first method is hidden inside the quotient rule here. Apply the rules correctly and the order you take them in does not matter.

**Watch out:** Expanding $\ln (1000 \cdot 1.08^t)$ as $t \cdot \ln (1000 \cdot 1.08)$ is **wrong**. The exponent sits only on $1.08$; the 1000 is not raised to it.

**Answer:** about 11.91 years.
