**Fikir:** Taban vektörlerini bir $B$ matrisinin sütunları yaparsak $c_1\mathbf{b}_1 + c_2\mathbf{b}_2 = B\mathbf{c}$ olur. Koordinatlar $B\mathbf{c} = \mathbf{x}$ denkleminin çözümü: $\mathbf{c} = B^{-1}\mathbf{x}$. Aynı tabanda birçok vektörün koordinatı istendiğinde $B^{-1}$ bir kez bulunur, her vektör için tek bir çarpım yeter.

**Adım 1 — Taban matrisi.**

$$
B = \begin{bmatrix} 1 & 1 \\ 2 & -1 \end{bmatrix}
$$

**Adım 2 — Determinant ve ters.** $\det B = 1 \cdot (-1) - 1 \cdot 2 = -3$. Yer değiştir, işaret çevir, $-3$'e böl:

$$
B^{-1} = \frac{1}{-3} \begin{bmatrix} -1 & -1 \\ -2 & 1 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 1 & 1 \\ 2 & -1 \end{bmatrix}
$$

**Adım 3 — $\mathbf{c} = B^{-1}\mathbf{x}$.**

$$
\begin{aligned}
\mathbf{c} &= \frac{1}{3} \begin{bmatrix} 1 \cdot 5 + 1 \cdot 1 \\ 2 \cdot 5 - 1 \cdot 1 \end{bmatrix} \\
&= \frac{1}{3} \begin{bmatrix} 6 \\ 9 \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Neden aynı sonuç?** Birinci yoldaki iki denklem tam olarak $B\mathbf{c} = \mathbf{x}$'in satırları. $\det B \ne 0$ olması da $\mathbf{b}_1$ ile $\mathbf{b}_2$'nin bağımsız, yani gerçekten bir taban olduğunu söylüyor.

**Cevap:** $(2, 3)$.
