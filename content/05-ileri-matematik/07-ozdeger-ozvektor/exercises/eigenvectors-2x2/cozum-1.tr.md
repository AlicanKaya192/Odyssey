**Ne soruluyor?** Her özdeğer için, $B$'nin yalnızca o kadar uzattığı doğrultu.

**Fikir:** $B\mathbf{v} = \lambda\mathbf{v}$'yi $(B - \lambda I)\mathbf{v} = \mathbf{0}$ olarak yaz. $\lambda$ gerçek bir özdeğer olduğu için $B - \lambda I$ tekil: iki satırı aynı bilgiyi veriyor, birini kullanmak yeter.

**Adım 1 — $\lambda = 2$.**

$$
B - 2I = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}
$$

İki satır da aynı: $2x + y = 0$. $x = 1$ koy: $y = -2$. Özvektör $(1, -2)$.

**Adım 2 — $\lambda = 5$.**

$$
B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}
$$

İlk satır $-x + y = 0$, yani $y = x$. $x = 1$ için $y = 1$. Özvektör $(1, 1)$. (İkinci satır $2x - 2y = 0$ aynı şeyi söylüyor.)

**Adım 3 — Sağla.** Özvektörü $B$ ile çarp:

$$
\begin{aligned}
B \begin{bmatrix} 1 \\ -2 \end{bmatrix} &= \begin{bmatrix} 4 - 2 \\ 2 - 6 \end{bmatrix} = \begin{bmatrix} 2 \\ -4 \end{bmatrix} = 2 \begin{bmatrix} 1 \\ -2 \end{bmatrix} \\
B \begin{bmatrix} 1 \\ 1 \end{bmatrix} &= \begin{bmatrix} 5 \\ 5 \end{bmatrix} = 5 \begin{bmatrix} 1 \\ 1 \end{bmatrix}
\end{aligned}
$$

İkisi de tutuyor. ✓

**Sonucu yorumla:** İki özvektör birbirine dik değil ($1 \cdot 1 + (-2) \cdot 1 = -1$). $B$ simetrik olmadığı için bu beklenen bir durum.

**Cevap:** $\lambda = 2$ için $y = -2$; $\lambda = 5$ için $y = 1$.
