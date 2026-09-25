**Ne soruluyor?** Ceza teriminin en iyi ağırlığı ve kaybın eğriliğini nasıl değiştirdiği.

**Fikir:** Kayıp $w$'nin dışbükey bir fonksiyonu; türevi sıfırlayan nokta genel en küçük.

**Adım 1 — Toplamlar.** $\sum x_i^2 = 1 + 4 = 5$, $\sum x_i y_i = 2 + 6 = 8$.

**Adım 2 — Türev.** $L'(w) = -2 \cdot 8 + 2 \cdot 5 w + 2\lambda w = 0$: $w = \frac{8}{5 + \lambda}$.

**Adım 3 — Değerler.** $\lambda = 0$: $w = \frac{8}{5} = 1{,}6$. $\lambda = 1$: $w = \frac{8}{6} = \frac{4}{3} \approx 1{,}333$.

**Adım 4 — Eğrilik.** $L''(w) = 2(5 + \lambda) = 12$.

**Sağlama:** Ceza ağırlığı sıfıra doğru çekti ($1{,}6 \to 1{,}33$); ridge'in işi bu. $L'' > 0$: kesin dışbükey ✓.

**Dikkat:** Ceza türevinde $2\lambda w$'yi unutmak $\lambda$'nın hiçbir etkisi yokmuş gibi $1{,}6$ verir.

**Cevap:** $\frac{8}{5}$, $\frac{4}{3}$ ve $12$.
