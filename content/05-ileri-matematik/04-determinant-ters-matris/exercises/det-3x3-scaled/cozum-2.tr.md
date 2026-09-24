**Fikir:** $3 \times 3$ için ezberlenebilecek bir kısayol: ilk iki sütunu sağa bir kez daha yaz. Soldan sağa aşağı inen üç köşegenin çarpımlarını topla, sağdan sola aşağı inen üçünü çıkar.

**Adım 1 — Genişletilmiş tablo.** $A$'nın yanına 1. ve 2. sütunu ekle:

$$
\begin{matrix} 2 & 0 & 1 & 2 & 0 \\ 1 & 3 & 2 & 1 & 3 \\ 1 & 1 & 2 & 1 & 1 \end{matrix}
$$

**Adım 2 — Aşağı sağa inen köşegenler (artı).**

$$
\begin{aligned}
2 \cdot 3 \cdot 2 &= 12 \\
0 \cdot 2 \cdot 1 &= 0 \\
1 \cdot 1 \cdot 1 &= 1
\end{aligned}
$$

Toplam $13$.

**Adım 3 — Aşağı sola inen köşegenler (eksi).**

$$
\begin{aligned}
1 \cdot 3 \cdot 1 &= 3 \\
2 \cdot 2 \cdot 1 &= 4 \\
0 \cdot 1 \cdot 2 &= 0
\end{aligned}
$$

Toplam $7$.

**Adım 4 — Fark.** $\det A = 13 - 7 = 6$, açılımla bulduğumuzun aynısı.

**Adım 5 — $\det(2A)$'yı kontrol et.** $2A$'nın her elemanı 2 katı; Sarrus'taki her çarpım **üç** eleman içerdiği için her çarpım $2^3 = 8$ katına çıkar. Farkları da 8 katına çıkar: $8 \cdot 6 = 48$.

**Dikkat:** Sarrus yalnızca $3 \times 3$'te geçerli; $4 \times 4$ ya da daha büyükte işe yaramaz. Oradaki yol açılım ya da Gauss eleme.

**Cevap:** $6$ ve $48$.
