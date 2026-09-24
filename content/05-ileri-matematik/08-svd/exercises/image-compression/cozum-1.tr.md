**Ne soruluyor?** SVD ile sıkıştırmanın kazancı: orijinal yerine ilk 30 katmanı saklarsak kaç sayı gerekir?

**Fikir:** Rankı $k$ olan yaklaşım $A_k = \sum_{i=1}^{k} \sigma_i\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$. Matrisin kendisini değil, her katmanın üç parçasını saklarız: $\mathbf{u}_i$ (satır sayısı kadar), $\mathbf{v}_i$ (sütun sayısı kadar) ve $\sigma_i$ (tek sayı).

**Adım 1 — Bir katman.** $m = 400$, $n = 600$:

$$
m + n + 1 = 400 + 600 + 1 = 1001 \text{ sayı}
$$

**Adım 2 — 30 katman.**

$$
k\,(m + n + 1) = 30 \cdot 1001 = 30\,030
$$

**Adım 3 — Orijinal.** Her piksel bir sayı:

$$
m \cdot n = 400 \cdot 600 = 240\,000
$$

**Adım 4 — Oran.**

$$
\frac{30\,030}{240\,000} \approx 0.1251 \quad \Rightarrow \quad \%12.5
$$

**Sonucu yorumla:** Orijinalin sekizde birinden az yer. Gerçek fotoğraflarda tekil değerler hızla küçüldüğü için 30 katman genellikle fotoğrafı gözün kolayca tanıyacağı kadar iyi koruyor; ayrıntı kaybı en küçük katmanlarda.

**Dikkat:** $k \cdot m \cdot n$ hesaplamak yanlış olur: $A_k$'yı tam matris olarak yeniden oluşturup saklarsan yine $240\,000$ sayı saklarsın. Kazanç, katmanların parçalarını ayrı saklamaktan geliyor.

**Cevap:** $30\,030$ sayı; yaklaşık %12.5.
