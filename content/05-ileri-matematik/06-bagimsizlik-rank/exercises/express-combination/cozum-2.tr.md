**Fikir:** "$\mathbf{v}_3$, $\mathbf{v}_1$ ile $\mathbf{v}_2$'nin germesinde mi?" sorusu, sütunları $\mathbf{v}_1, \mathbf{v}_2$ olan sistemin sağ tarafı $\mathbf{v}_3$ iken çözümü olup olmadığı sorusu. Artırılmış matrisi eleyelim; aynı eleme rankı da gösterir.

**Adım 1 — Artırılmış matris** $[\mathbf{v}_1\ \mathbf{v}_2 \mid \mathbf{v}_3]$:

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 2 & 1 & 7 \end{array}\right]
$$

**Adım 2 — $R_3 \to R_3 - 2R_1$.** $(2 - 2,\ 1 - 0 \mid 7 - 4)$:

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 0 & 1 & 3 \end{array}\right]
$$

**Adım 3 — $R_3 \to R_3 - R_2$.**

$$
\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 3 \\ 0 & 0 & 0 \end{array}\right]
$$

Son satır $0 = 0$: çelişki yok, çözüm var. İlk iki satırdan $a = 2$, $b = 3$.

**Adım 4 — Rank.** Üç vektörü sütun yapan $3 \times 3$ matriste aynı eleme yapılır; sol taraf aynı kaldığı için pivotlar yine yalnızca 1. ve 2. sütunda. $\operatorname{rank} = 2$, determinant $0$.

**Neden aynı sonuç?** $\operatorname{rank}\,[\mathbf{v}_1\ \mathbf{v}_2] = \operatorname{rank}\,[\mathbf{v}_1\ \mathbf{v}_2 \mid \mathbf{v}_3] = 2$: sağ taraf yeni bir pivot getirmedi, yani $\mathbf{v}_3$ yeni bir yön eklemiyor.

**Cevap:** $2$, $3$ ve rank $2$.
