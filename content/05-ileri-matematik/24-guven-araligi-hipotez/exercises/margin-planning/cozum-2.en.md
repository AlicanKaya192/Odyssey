**Idea:** The margin of error is proportional to $\frac{z^{*}}{\sqrt{n}}$. Work by ratio from a known point ($n = 100$, $E = 3.92$).

**Step 1 — Start.** $3.92$ at $n = 100$.

**Step 2 — 95 percent, $E = 2$.** To shrink the margin $\frac{3.92}{2} = 1.96$ times, $n$ grows $1.96^2 = 3.8416$ times: $384.16$, so $385$.

**Step 3 — 99 percent.** $z^{*}$ grows by $\frac{2.576}{1.96}$; to keep the same margin, $n$ must grow by that ratio squared, $1.7274$ times: $384.16 \cdot 1.7274 \approx 663.6$, so $664$.

**Why the same result?** $n$ is proportional to $(z^{*})^2$ and inversely proportional to $E^2$; working by ratios applies the formula piece by piece.

**Answer:** $3.92$, $385$ and $664$.
