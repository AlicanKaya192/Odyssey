**Fikir:** $X + Y = w^\mathsf{T}(X, Y)$, $w = (1, 1)$; varyansı $w^\mathsf{T}\Sigma w$.

**Adım 1 — Matris.** $\Sigma = \begin{pmatrix} 25 & 12 \\ 12 & 36 \end{pmatrix}$; köşegen dışı $r\sigma_X\sigma_Y = 12$.

**Adım 2 — Toplam.** $w = (1, 1)$: $w^\mathsf{T}\Sigma w$ matrisin bütün elemanlarının toplamı, $25 + 12 + 12 + 36 = 85$.

**Adım 3 — Fark.** $w = (1, -1)$: köşegen dışı terimler eksi işaret alır, $25 - 12 - 12 + 36 = 37$.

**Neden aynı sonuç?** $w^\mathsf{T}\Sigma w = \sum_{i,j} w_i w_j \Sigma_{ij}$; iki değişkende bu tam olarak $\operatorname{Var}X + \operatorname{Var}Y \pm 2\operatorname{Cov}$.

**Cevap:** $12$; $85$ ve $37$.
