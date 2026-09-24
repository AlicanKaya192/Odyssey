**Fikir:** Her sıranın tek bir matrisi var. "Önce $R$, sonra $S$" $= SR$; "önce $S$, sonra $R$" $= RS$. İki çarpımı hesaplayıp $\mathbf{v}$'ye uygularız; matrislere bakınca her sıranın **ne tür bir dönüşüm** olduğunu da görürüz.

**Adım 1 — $SR$.** Satır çarpı sütun:

$$
SR = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}
$$

**Adım 2 — $RS$.**

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

**Adım 3 — $\mathbf{v}$'ye uygula.**

$$
\begin{aligned}
SR \begin{bmatrix} 1 \\ 3 \end{bmatrix} &= \begin{bmatrix} -3 \\ -1 \end{bmatrix} \\
RS \begin{bmatrix} 1 \\ 3 \end{bmatrix} &= \begin{bmatrix} 3 \\ 1 \end{bmatrix}
\end{aligned}
$$

**Matrisleri oku:** $RS = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ bileşenlerin yerini değiştiriyor: $(x, y) \to (y, x)$, yani $y = x$ doğrusuna göre yansıma. $SR$ ise $(x, y) \to (-y, -x)$: $y = -x$ doğrusuna göre yansıma. Bir döndürme ile bir yansıma art arda yapılınca yine bir yansıma çıkıyor, ama **hangi ayna** olduğu sıraya bağlı.

**Cevap:** $(-3, -1)$ ve $(3, 1)$.
