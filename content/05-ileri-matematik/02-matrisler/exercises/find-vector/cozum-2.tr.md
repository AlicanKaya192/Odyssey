**Fikir:** Aynı çarpıma sütun gözüyle bak. $A\mathbf{x}$, $A$'nın sütunlarının $\mathbf{x}$'in bileşenleriyle ağırlıklı toplamı. O zaman soru şuna dönüşüyor: $(7, 2)$ vektörünü $(2, 1)$ ve $(1, -1)$ sütunlarından hangi katsayılarla kurarım?

**Adım 1 — Sütunlarla yaz.**

$$
x_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + x_2 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 7 \\ 2 \end{bmatrix}
$$

**Adım 2 — Bileşenleri eşitle.** Üst bileşenler: $2x_1 + x_2 = 7$. Alt bileşenler: $x_1 - x_2 = 2$.

**Adım 3 — Alt denklemden $x_1$'i çek.**

$$
x_1 = 2 + x_2
$$

**Adım 4 — Üst denkleme koy.**

$$
\begin{aligned}
2(2 + x_2) + x_2 &= 7 \\
4 + 2x_2 + x_2 &= 7 \\
3x_2 &= 3 \\
x_2 &= 1
\end{aligned}
$$

Buradan $x_1 = 2 + 1 = 3$.

**Sağlama:** Sütunları bu katsayılarla topla:

$$
\begin{aligned}
3 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} &= \begin{bmatrix} 6 \\ 3 \end{bmatrix} + \begin{bmatrix} 1 \\ -1 \end{bmatrix} \\
&= \begin{bmatrix} 7 \\ 2 \end{bmatrix}
\end{aligned}
$$

Tutuyor. ✓

**Ne gördük?** "$A\mathbf{x} = \mathbf{b}$'yi çöz" ile "$\mathbf{b}$'yi $A$'nın sütunlarından kur" aynı soru. Gauss eleme bölümünde bunu büyük sistemler için düzenli bir yöntemle yapacağız.

**Cevap:** $x_1 = 3$, $x_2 = 1$.
