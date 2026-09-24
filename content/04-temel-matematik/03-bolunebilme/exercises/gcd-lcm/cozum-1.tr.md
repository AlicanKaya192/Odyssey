**Ne soruluyor?** İki sayıyı da bölen en büyük sayı ve iki sayının da katı olan en küçük sayı.

**Fikir:** Asal çarpanlar bir sayının yapı taşları. Bir sayının bölenleri, onun asal çarpanlarından bir kısmıyla kurulur; katları ise en az o çarpanların hepsini içerir. EBOB için ikisinde de olan kadarını, EKOK için ikisinden birinde olan kadarını alırız.

**Adım 1 — $84$'ü ayır.**

$$
84 = 2 \cdot 42 = 2 \cdot 2 \cdot 21 = 2^2 \cdot 3 \cdot 7
$$

**Adım 2 — $126$'yı ayır.**

$$
126 = 2 \cdot 63 = 2 \cdot 3 \cdot 21 = 2 \cdot 3^2 \cdot 7
$$

**Adım 3 — EBOB: ortak asallar, küçük üsler.** Ortak asallar $2$, $3$, $7$. Üsler: $2$ için $\min(2, 1) = 1$, $3$ için $\min(1, 2) = 1$, $7$ için $1$.

$$
\text{EBOB} = 2 \cdot 3 \cdot 7 = 42
$$

**Adım 4 — EKOK: bütün asallar, büyük üsler.** $2$ için $2$, $3$ için $2$, $7$ için $1$:

$$
\text{EKOK} = 2^2 \cdot 3^2 \cdot 7 = 4 \cdot 9 \cdot 7 = 252
$$

**Sağlama:** $84 = 42 \cdot 2$ ve $126 = 42 \cdot 3$ ✓. $252 = 84 \cdot 3 = 126 \cdot 2$ ✓. Ayrıca $42 \cdot 252 = 10\,584 = 84 \cdot 126$ ✓.

**Cevap:** EBOB $42$, EKOK $252$.
