**Fikir:** Jacobian'ın $j$'nci sütunu, yalnızca $j$'nci girdi biraz değişince çıktıların nasıl değiştiği. Küçük bir adım atıp farkı adıma böl.

**Adım 1 — Birinci sütun.** $x$'i $0{,}01$ artır: $F(1{,}01; 2) = (2{,}0402; \ 7{,}01)$, $F(1, 2) = (2, 7)$. Fark bölü $0{,}01$: $(4{,}02; \ 1)$ $\approx (4, 1)$.

**Adım 2 — İkinci sütun.** $y$'yi $0{,}01$ artır: $F(1; 2{,}01) = (2{,}01; \ 7{,}03)$. Fark bölü $0{,}01$: $(1, 3)$.

**Adım 3 — Determinant.** $\begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}$: $12 - 1 = 11$.

**Neden aynı sonuç?** Kısmi türev tam olarak bu oranın limiti; $4{,}02$'deki fazlalık adımın sonlu olmasından ($h \to 0$ iken $4$'e gider). Gradyan kontrolünün Jacobian hâli: kodda yazılmış bir Jacobian'ı sütun sütun böyle doğrulamak mümkün.

**Cevap:** $4$, $1$, $11$.
