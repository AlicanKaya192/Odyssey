**Ne soruluyor?** $3A - 2B$ yeni bir $2 \times 2$ matris. Onun dört elemanını arıyoruz.

**Fikir:** Matrislerde skalerle çarpma ve çıkarma, vektörlerdeki gibi **eleman eleman** yapılır. Önce çarpmalar, sonra çıkarma:

- Matrisi bir sayıyla çarpmak, her elemanını o sayıyla çarpmak.
- İki matrisi çıkarmak, aynı yerdeki elemanları çıkarmak (iki matris de aynı boyutta olmalı; burada ikisi de $2 \times 2$).

**Adım 1 — $A$'yı 3 ile çarp.** Dört elemanın her biri 3 katına çıkıyor:

$$
3A = \begin{bmatrix} 3 \cdot 2 & 3 \cdot (-1) \\ 3 \cdot 0 & 3 \cdot 3 \end{bmatrix} = \begin{bmatrix} 6 & -3 \\ 0 & 9 \end{bmatrix}
$$

**Adım 2 — $B$'yi 2 ile çarp.**

$$
2B = \begin{bmatrix} 2 \cdot 1 & 2 \cdot 4 \\ 2 \cdot (-2) & 2 \cdot 1 \end{bmatrix} = \begin{bmatrix} 2 & 8 \\ -4 & 2 \end{bmatrix}
$$

**Adım 3 — Aynı yerdeki elemanları çıkar.** Sol üst eksi sol üst, sağ üst eksi sağ üst, ve böyle devam:

$$
\begin{aligned}
c_{11} &= 6 - 2 = 4 \\
c_{12} &= -3 - 8 = -11 \\
c_{21} &= 0 - (-4) = 4 \\
c_{22} &= 9 - 2 = 7
\end{aligned}
$$

$$
C = \begin{bmatrix} 4 & -11 \\ 4 & 7 \end{bmatrix}
$$

**Dikkat:** $c_{21}$'de negatif bir sayı çıkarılıyor: $0 - (-4) = +4$. Burada $-4$ yazmak en sık hata.

**Cevap:** $c_{11} = 4$, $c_{12} = -11$, $c_{21} = 4$, $c_{22} = 7$.
