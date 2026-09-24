**Fikir:** Art arda iki dönüşüm, çarpımları olan tek bir dönüşüme eşit: $S(R\mathbf{x}) = (SR)\mathbf{x}$. Önce $SR$'yi bulur, sonra noktayı bir kez çarparız. Aynı dönüşüm birçok noktaya uygulanacaksa bu yol çok daha hızlı.

**Adım 1 — Sırayı doğru yaz.** "Önce $R$, sonra $S$" sağdan sola okunur: $SR$.

**Adım 2 — Çarpımı hesapla.** Satır çarpı sütun:

$$
\begin{aligned}
SR &= \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \\
&= \begin{bmatrix} 2 \cdot 0 + 0 \cdot 1 & 2 \cdot (-1) + 0 \cdot 0 \\ 0 \cdot 0 + 1 \cdot 1 & 0 \cdot (-1) + 1 \cdot 0 \end{bmatrix} \\
&= \begin{bmatrix} 0 & -2 \\ 1 & 0 \end{bmatrix}
\end{aligned}
$$

**Adım 3 — Noktaya uygula.**

$$
\begin{bmatrix} 0 & -2 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

**Sağlama:** $SR$'nin sütunları $\mathbf{e}_1$ ve $\mathbf{e}_2$'nin vardığı yer olmalı. $\mathbf{e}_1$ dönünce $(0, 1)$, esneyince yine $(0, 1)$: 1. sütun $(0, 1)$. ✓ $\mathbf{e}_2$ dönünce $(-1, 0)$, esneyince $(-2, 0)$: 2. sütun $(-2, 0)$. ✓

**Cevap:** $(-2, 3)$.
