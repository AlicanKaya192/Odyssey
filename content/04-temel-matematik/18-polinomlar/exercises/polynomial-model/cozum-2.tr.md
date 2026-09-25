**Fikir:** Polinom regresyonu, $x$'ten yeni özellikler üretip doğrusal bir model kurar. Özellik vektörü $(1, x, x^2, x^3)$, ağırlık vektörü $(w_0, w_1, w_2, w_3)$; tahmin ikisinin karşılıklı çarpımlarının toplamı.

**Adım 1 — $x = 2$.** Özellikler $(1, 2, 4, 8)$, ağırlıklar $(1, 2, -1, 0{,}5)$:

$$
\begin{aligned}
&1 \cdot 1 + 2 \cdot 2 + 4 \cdot (-1) + 8 \cdot 0{,}5 \\
&= 1 + 4 - 4 + 4 = 5
\end{aligned}
$$

**Adım 2 — $x = -2$.** Özellikler $(1, -2, 4, -8)$:

$$
1 - 4 - 4 - 4 = -11
$$

**Adım 3 — Hata.** $6 - 5 = 1$.

**Neden aynı sonuç?** Karşılıklı çarpımları toplamak, polinomu terim terim hesaplamanın kendisi; yalnızca kuvvetleri önceden bir listeye yazdık. Bu bakış, modelin neden "$w$'lere göre doğrusal" olduğunu da gösteriyor: $w$'ler yalnızca birer çarpan.

**Cevap:** $5$, $-11$ ve $1$.
