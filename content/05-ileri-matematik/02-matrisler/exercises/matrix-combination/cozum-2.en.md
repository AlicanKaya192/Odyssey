**Idea:** Since scaling and subtraction work entry by entry, entries never mix. The entry of $C$ in row $i$, column $j$ comes only from the entries of $A$ and $B$ in the same position:

$$
c_{ij} = 3\,a_{ij} - 2\,b_{ij}
$$

So each entry can be computed on one line, without writing any intermediate matrix.

**Step 1 — Pair up the entries.** Pairs in the same position: top left $(2,\ 1)$, top right $(-1,\ 4)$, bottom left $(0,\ -2)$, bottom right $(3,\ 1)$. In each pair the first number is from $A$, the second from $B$.

**Step 2 — Apply the formula to each pair.**

$$
\begin{aligned}
c_{11} &= 3 \cdot 2 - 2 \cdot 1 = 6 - 2 = 4 \\
c_{12} &= 3 \cdot (-1) - 2 \cdot 4 = -3 - 8 = -11 \\
c_{21} &= 3 \cdot 0 - 2 \cdot (-2) = 0 + 4 = 4 \\
c_{22} &= 3 \cdot 3 - 2 \cdot 1 = 9 - 2 = 7
\end{aligned}
$$

**When does it help?** If a question asks for just one entry of a large matrix, this is much faster: no need to compute the whole matrix, you only look at the two numbers in that position.

**Answer:** $4$, $-11$, $4$, $7$.
