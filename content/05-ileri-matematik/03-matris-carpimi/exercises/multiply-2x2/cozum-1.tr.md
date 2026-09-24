**Ne soruluyor?** İki $2 \times 2$ matrisin çarpımı; sonuç da $2 \times 2$, yani dört sayı.

**Fikir:** Matris çarpımı eleman eleman yapılmaz. $C$'nin $i$. satır, $j$. sütundaki elemanı, $A$'nın $i$. satırı ile $B$'nin $j$. sütununun **nokta çarpımı**: karşılıklı sayıları çarp, topla.

Önce satırları ve sütunları ayır:

- $A$'nın satırları: $(2, -1)$ ve $(3, 4)$
- $B$'nin sütunları: $(1, 0)$ ve $(2, -3)$

**Adım 1 — $c_{11}$:** 1. satır ile 1. sütun.

$$
c_{11} = 2 \cdot 1 + (-1) \cdot 0 = 2 + 0 = 2
$$

**Adım 2 — $c_{12}$:** 1. satır ile 2. sütun.

$$
\begin{aligned}
c_{12} &= 2 \cdot 2 + (-1) \cdot (-3) \\
&= 4 + 3 = 7
\end{aligned}
$$

**Adım 3 — $c_{21}$:** 2. satır ile 1. sütun.

$$
c_{21} = 3 \cdot 1 + 4 \cdot 0 = 3
$$

**Adım 4 — $c_{22}$:** 2. satır ile 2. sütun.

$$
\begin{aligned}
c_{22} &= 3 \cdot 2 + 4 \cdot (-3) \\
&= 6 - 12 = -6
\end{aligned}
$$

$$
C = \begin{bmatrix} 2 & 7 \\ 3 & -6 \end{bmatrix}
$$

**Dikkat:** Eleman eleman çarpsaydın $\begin{bmatrix} 2 & -2 \\ 0 & -12 \end{bmatrix}$ bulurdun. O başka bir işlem (Hadamard çarpımı).

**Cevap:** $c_{11} = 2$, $c_{12} = 7$, $c_{21} = 3$, $c_{22} = -6$.
