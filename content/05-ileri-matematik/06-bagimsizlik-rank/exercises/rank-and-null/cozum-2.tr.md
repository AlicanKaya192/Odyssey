**Fikir:** $A\mathbf{x} = \mathbf{0}$ demek $x \cdot (\text{1. sütun}) + y \cdot (\text{2. sütun}) + z \cdot (\text{3. sütun}) = \mathbf{0}$ demek. Yani çekirdek, sütunlar arasındaki bağımlılıkları arıyor. Doğrudan sütunlara bakalım.

**Adım 1 — Sütunları yaz.**

$$
\begin{aligned}
\mathbf{a}_1 &= (1, 2, 1) \\
\mathbf{a}_2 &= (2, 4, 1) \\
\mathbf{a}_3 &= (3, 6, 1)
\end{aligned}
$$

**Adım 2 — İlk ikisi bağımsız mı?** $\mathbf{a}_2$, $\mathbf{a}_1$'in katı değil (1. bileşende 2 kat, 3. bileşende 1 kat). İkisi bağımsız: rank en az 2.

**Adım 3 — Üçüncü, ilk ikisinin kombinasyonu mu?** $\mathbf{a}_3 = p\,\mathbf{a}_1 + q\,\mathbf{a}_2$ arayalım. 1. ve 3. bileşenler:

$$
\begin{aligned}
p + 2q &= 3 \\
p + q &= 1
\end{aligned}
$$

Çıkarınca $q = 2$, sonra $p = -1$. 2. bileşenle sına: $-1 \cdot 2 + 2 \cdot 4 = 6$ ✓. Yani $\mathbf{a}_3 = -\mathbf{a}_1 + 2\mathbf{a}_2$: üçüncü sütun fazlalık, rank tam olarak $2$.

**Adım 4 — Bağı çekirdek vektörüne çevir.** Her şeyi bir tarafa topla:

$$
\mathbf{a}_1 - 2\mathbf{a}_2 + \mathbf{a}_3 = \mathbf{0}
$$

Katsayılar $(1, -2, 1)$: bu vektör çekirdekte ve $z = 1$ olan çözüm tam olarak bu.

**Neden işe yarar?** Çekirdek vektörleri, sütunları sıfıra götüren "tarifler". Birinci yol bu tarifi elemeyle, bu yol doğrudan sütunlara bakarak buldu.

**Cevap:** $2$; $x = 1$, $y = -2$.
