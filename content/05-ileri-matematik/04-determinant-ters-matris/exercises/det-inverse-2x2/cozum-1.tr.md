**Ne soruluyor?** Önce determinant, sonra ters. Sıra önemli: determinant sıfır çıksaydı ters olmayacaktı.

**Fikir:** $2 \times 2$ için

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Burada $a = 4$, $b = 7$, $c = 2$, $d = 6$.

**Adım 1 — Determinant.** Ana köşegenin çarpımı eksi öteki köşegenin çarpımı:

$$
\det A = 4 \cdot 6 - 7 \cdot 2 = 24 - 14 = 10
$$

Sıfır değil; ters var. Ayrıca $A$ alanları 10 katına çıkarıyor, tersi de 10'a bölecek.

**Adım 2 — Yer değiştir, işaret çevir.** $4$ ile $6$ yer değiştiriyor; $7$ ve $2$ yerinde kalıyor ama işaretleri değişiyor:

$$
\begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix}
$$

**Adım 3 — Determinanta böl.** Her elemanı $10$'a böl:

$$
A^{-1} = \frac{1}{10} \begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}
$$

**Sağlama:** $A$ ile bölmeden önceki matrisi çarp; $10I$ çıkmalı:

$$
\begin{aligned}
\begin{bmatrix} 4 & 7 \\ 2 & 6 \end{bmatrix} \begin{bmatrix} 6 & -7 \\ -2 & 4 \end{bmatrix} &= \begin{bmatrix} 24 - 14 & -28 + 28 \\ 12 - 12 & -14 + 24 \end{bmatrix} \\
&= \begin{bmatrix} 10 & 0 \\ 0 & 10 \end{bmatrix}
\end{aligned}
$$

$10$'a bölünce $I$. ✓

**Dikkat:** $7$ ile $2$'nin **yeri değişmez**, yalnızca işaretleri. Yerlerini de değiştirmek en sık yapılan hata.

**Cevap:** $\det A = 10$; $A^{-1} = \begin{bmatrix} 0.6 & -0.7 \\ -0.2 & 0.4 \end{bmatrix}$.
