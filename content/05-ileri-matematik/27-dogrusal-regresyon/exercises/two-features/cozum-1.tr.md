**Ne soruluyor?** Normal denklemlerin $2 \times 2$ çözümü.

**Fikir:** $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$.

**Adım 1 — Determinant.** $4 \cdot 2 - 2 \cdot 2 = 4$.

**Adım 2 — Ters.** $\frac{1}{4}\begin{pmatrix} 2 & -2 \\ -2 & 4 \end{pmatrix}$.

**Adım 3 — Çarpım.**

$$
w = \frac{1}{4}\begin{pmatrix} 2 \cdot 10 - 2 \cdot 6 \\ -2 \cdot 10 + 4 \cdot 6 \end{pmatrix} = \frac{1}{4}\begin{pmatrix} 8 \\ 4 \end{pmatrix} = \begin{pmatrix} 2 \\ 1 \end{pmatrix}
$$

**Sağlama:** $X^\mathsf{T}Xw = (4 \cdot 2 + 2 \cdot 1, \ 2 \cdot 2 + 2 \cdot 1) = (10, 6)$ ✓.

**Dikkat:** Ters matriste köşegen elemanlar yer değiştirir, köşegen dışındakilerin yalnızca işareti değişir.

**Cevap:** $4$; $2$; $1$.
