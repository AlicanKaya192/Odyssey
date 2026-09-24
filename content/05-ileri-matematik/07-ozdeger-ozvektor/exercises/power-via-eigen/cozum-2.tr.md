**Fikir:** Köşegenleştirme $A = PDP^{-1}$ ile $A^k$'yı $k$ cinsinden bir kez yaz; sonra $k = 5$ koy. Hem sonucu hem de bir sağlama yolu verir.

**Adım 1 — $P$, $D$, $P^{-1}$.** Özvektörler sütunlarda, özdeğerler köşegende:

$$
P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}
\qquad
D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}
$$

$\det P = -2$, öyleyse $P^{-1} = \tfrac{1}{2}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$.

**Adım 2 — $A^k = PD^kP^{-1}$.** $D^k$'nın köşegeni $3^k$ ve $1$:

$$
\begin{aligned}
A^k &= \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} 3^k & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \\
&= \frac{1}{2} \begin{bmatrix} 3^k + 1 & 3^k - 1 \\ 3^k - 1 & 3^k + 1 \end{bmatrix}
\end{aligned}
$$

Sağlama $k = 1$: $\tfrac{1}{2}\begin{bmatrix} 4 & 2 \\ 2 & 4 \end{bmatrix} = A$ ✓.

**Adım 3 — $k = 5$.** $3^5 = 243$:

$$
A^5 = \frac{1}{2} \begin{bmatrix} 244 & 242 \\ 242 & 244 \end{bmatrix} = \begin{bmatrix} 122 & 121 \\ 121 & 122 \end{bmatrix}
$$

**Adım 4 — Vektöre uygula.**

$$
\begin{aligned}
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} &= \begin{bmatrix} 366 + 121 \\ 363 + 122 \end{bmatrix} \\
&= \begin{bmatrix} 487 \\ 485 \end{bmatrix}
\end{aligned}
$$

**Neden aynı sonuç?** Birinci yolda $P^{-1}$ ile çarpmak yerine vektörü doğrudan özvektörlere ayırdık; bu, $P^{-1}\mathbf{x}$'i hesaplamanın ta kendisi ($c_1 = 2$, $c_2 = 1$).

**Cevap:** $487$ ve $485$.
