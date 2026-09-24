**Fikir:** $2 \times 2$'de $A^\mathsf{T}A$'yı hiç yazmadan iki bilgiyle yetinebiliriz:

- $\sigma_1^2 + \sigma_2^2$ = $A$'nın bütün elemanlarının kareleri toplamı,
- $\sigma_1 \sigma_2 = |\det A|$ (döndürmeler alanı değiştirmez, alan çarpanı yalnızca $\Sigma$'dan gelir).

Toplamı ve çarpımı bilinen iki sayı bulmak, önceki bölümdeki iz–determinant kısayolunun aynısı.

**Adım 1 — Kareler toplamı.**

$$
\sigma_1^2 + \sigma_2^2 = 3^2 + 0^2 + 4^2 + 5^2 = 50
$$

**Adım 2 — Determinant.**

$$
\sigma_1\sigma_2 = |3 \cdot 5 - 0 \cdot 4| = 15
$$

Öyleyse $\sigma_1^2 \sigma_2^2 = 225$.

**Adım 3 — Kareleri bul.** $\sigma_1^2$ ve $\sigma_2^2$, toplamı $50$, çarpımı $225$ olan iki sayı: $45$ ve $5$.

**Adım 4 — Karekök.** $\sigma_1 = \sqrt{45} \approx 6.71$, $\sigma_2 = \sqrt{5} \approx 2.24$.

**Neden aynı sonuç?** $\sigma_1^2 + \sigma_2^2 = \operatorname{tr}(A^\mathsf{T}A)$ ve $\sigma_1^2\sigma_2^2 = \det(A^\mathsf{T}A)$. Birinci yolda karakteristik denklemi kurarken kullandığımız iki sayı tam olarak bunlardı; burada onları doğrudan $A$'dan okuduk.

**Sonucu yorumla:** $A$ bir yönde yaklaşık $6.7$ katına, dik yönde yalnızca $2.2$ katına esnetiyor. Koşul sayısı $6.71 / 2.24 = 3$.

**Cevap:** $6.71$ ve $2.24$.
