**Fikir:** Skalerle çarpma ve çıkarma eleman eleman yapıldığı için elemanlar birbirine karışmaz. $C$'nin $i$. satır, $j$. sütundaki elemanı yalnızca $A$ ve $B$'nin aynı yerdeki elemanlarından gelir:

$$
c_{ij} = 3\,a_{ij} - 2\,b_{ij}
$$

Böylece her elemanı ara matris yazmadan, tek satırda hesaplayabiliriz.

**Adım 1 — Elemanları eşleştir.** Aynı yerdeki çiftler: sol üst $(2,\ 1)$, sağ üst $(-1,\ 4)$, sol alt $(0,\ -2)$, sağ alt $(3,\ 1)$. Her çiftte ilk sayı $A$'dan, ikincisi $B$'den.

**Adım 2 — Her çifte formülü uygula.**

$$
\begin{aligned}
c_{11} &= 3 \cdot 2 - 2 \cdot 1 = 6 - 2 = 4 \\
c_{12} &= 3 \cdot (-1) - 2 \cdot 4 = -3 - 8 = -11 \\
c_{21} &= 3 \cdot 0 - 2 \cdot (-2) = 0 + 4 = 4 \\
c_{22} &= 3 \cdot 3 - 2 \cdot 1 = 9 - 2 = 7
\end{aligned}
$$

**Ne zaman işe yarar?** Büyük bir matriste yalnızca bir eleman sorulursa bu yol çok daha hızlı: bütün matrisi hesaplamak gerekmiyor, yalnızca o yerdeki iki sayıya bakıyorsun.

**Cevap:** $4$, $-11$, $4$, $7$.
