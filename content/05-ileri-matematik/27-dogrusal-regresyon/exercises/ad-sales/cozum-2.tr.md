**Fikir:** $X$'in sütunları $(1, 1, 1, 1, 1)$ ve $x$; $X^\mathsf{T}Xw = X^\mathsf{T}y$'yi çöz.

**Adım 1 — Matrisler.** $X^\mathsf{T}X = \begin{pmatrix} 5 & 15 \\ 15 & 55 \end{pmatrix}$, $X^\mathsf{T}y = \begin{pmatrix} 25 \\ 83 \end{pmatrix}$ ($\sum xy = 3 + 10 + 12 + 28 + 30 = 83$).

**Adım 2 — Çözüm.** Determinant $50$.

$$
\begin{pmatrix} b \\ w \end{pmatrix} = \frac{1}{50}\begin{pmatrix} 55 \cdot 25 - 15 \cdot 83 \\ -15 \cdot 25 + 5 \cdot 83 \end{pmatrix} = \frac{1}{50}\begin{pmatrix} 130 \\ 40 \end{pmatrix}
$$

$b = 2{,}6$, $w = 0{,}8$.

**Adım 3 — Tahmin.** $(1, 6) \cdot (2{,}6; \ 0{,}8) = 7{,}4$.

**Neden aynı sonuç?** Sapma formülü, normal denklemlerin $2 \times 2$ sistemini elle çözüp sadeleştirmekle elde ediliyor; ikisi aynı denklemlerin çözümü.

**Cevap:** $0{,}8$; $2{,}6$ ve $7{,}4$.
