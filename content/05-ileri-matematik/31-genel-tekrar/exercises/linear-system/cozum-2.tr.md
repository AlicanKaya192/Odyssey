**Fikir:** $x_i = \frac{\det A_i}{\det A}$; $A_i$, $A$'nın $i$. sütunu yerine $b$ yazılmış hâli.

**Adım 1 — $\det A$.** $10$.

**Adım 2 — $x_1$.** $\det\begin{pmatrix} 7 & 1 \\ 8 & 4 \end{pmatrix} = 28 - 8 = 20$; $x_1 = 2$.

**Adım 3 — $x_2$.** $\det\begin{pmatrix} 3 & 7 \\ 2 & 8 \end{pmatrix} = 24 - 14 = 10$; $x_2 = 1$.

**Neden aynı sonuç?** $A^{-1}b$'nin her bileşeni açılınca tam bu determinant oranları çıkar; Cramer kuralı ters matrisle çarpmanın bileşen bileşen yazılışı. Küçük sistemlerde pratik, büyüklerde Gauss eleme daha ucuz.

**Cevap:** $10$; $2$ ve $1$.
