**Idea:** Look at the number of mistakes instead of accuracy; accuracy $= 100\% -$ error percentage. Counting mistakes also shows where each model goes wrong.

**Step 1 — The model's mistakes.** $2\,200 - 1\,870 = 330$ wrong:

$$
\frac{330}{2\,200} = 0.15 = 15\% \quad\Rightarrow\quad \text{accuracy } 85\%
$$

**Step 2 — The always-"normal" model's mistakes.** It only gets the $110$ fraud cases wrong:

$$
\frac{110}{2\,200} = 0.05 = 5\% \quad\Rightarrow\quad \text{accuracy } 95\%
$$

**Step 3 — What the mistakes are.** All $110$ mistakes of the always-"normal" model are fraud: exactly the cases that must be caught. We do not know how many of the trained model's $330$ mistakes are fraud; perhaps it catches most of them.

**Why the same result?** The correct and wrong percentages add up to $100\%$; either route reaches the same numbers. The advantage of this route is that it forces the question of **which class** the mistakes are in.

**Answer:** $85\%$ and $95\%$.
