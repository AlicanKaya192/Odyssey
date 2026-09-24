**What is asked?** How much of the matrix remains when the first two layers are kept and the last two dropped, and how large the error is.

**Idea:** $A = \sum \sigma_i\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$. The best rank-2 approximation is the first two layers (Eckart–Young). The sum of the squares of the entries is $\sum \sigma_i^2$, so "energy" is computed with squares and the error of the dropped part comes from the dropped squares.

**Step 1 — The squares.**

$$
\begin{aligned}
\sigma_1^2 &= 144 \\
\sigma_2^2 &= 25 \\
\sigma_3^2 &= 9 \\
\sigma_4^2 &= 1
\end{aligned}
$$

The total energy is $179$.

**Step 2 — The share kept.**

$$
\frac{144 + 25}{179} = \frac{169}{179} \approx 0.944
$$

**Step 3 — The error.** The dropped layers are $\sigma_3$ and $\sigma_4$:

$$
\begin{aligned}
\|A - A_2\| &= \sqrt{\sigma_3^2 + \sigma_4^2} \\
&= \sqrt{9 + 1} = \sqrt{10} \approx 3.16
\end{aligned}
$$

**Check:** Kept plus dropped energy: $169 + 10 = 179$ ✓.

**Watch out:** Taking the ratio of the singular values themselves ($\tfrac{12 + 5}{21} \approx 0.81$) is wrong; use squares. Squaring makes the share of small singular values even smaller: here two layers carry 94% of the matrix.

**Answer:** $0.94$ and $3.16$.
