**Ne soruluyor?** Rankı 1 olan bir matrisin tekil değerleri: kaç tane sıfır olmayan var ve ne kadar büyük?

**Fikir:** Rank = sıfır olmayan tekil değer sayısı. Rankı 1 olan bir matris tek bir katmandır: $A = \mathbf{a}\mathbf{b}^\mathsf{T}$. Böyle bir matriste tek tekil değer $\sigma_1 = \|\mathbf{a}\|\,\|\mathbf{b}\|$.

**Adım 1 — Rank.** İki sütun da $(2, 1)$: sütunlar bağımlı, rank $1$. Öyleyse $\sigma_2 = 0$.

**Adım 2 — Sütun çarpı satır olarak yaz.** Her satır $(1, 1)$'in katı ($2$ ve $1$ katı):

$$
A = \begin{bmatrix} 2 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \end{bmatrix}
$$

**Adım 3 — Uzunlukları birim vektörlere çevir.** $\mathbf{a} = (2, 1)$, $\|\mathbf{a}\| = \sqrt{5}$; $\mathbf{b} = (1, 1)$, $\|\mathbf{b}\| = \sqrt{2}$:

$$
A = \sqrt{5}\sqrt{2} \cdot \underbrace{\tfrac{1}{\sqrt{5}}\begin{bmatrix} 2 \\ 1 \end{bmatrix}}_{\mathbf{u}_1} \underbrace{\tfrac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \end{bmatrix}}_{\mathbf{v}_1^\mathsf{T}}
$$

**Adım 4 — Tekil değer.**

$$
\sigma_1 = \sqrt{5} \cdot \sqrt{2} = \sqrt{10} \approx 3.16
$$

**Sağlama:** Elemanların kareleri toplamı $4 + 4 + 1 + 1 = 10 = \sigma_1^2 + \sigma_2^2$ ✓.

**Sonucu yorumla:** $A$ bütün düzlemi $\mathbf{u}_1 = (2, 1)/\sqrt{5}$ doğrultusundaki bir doğruya eziyor; birim çember bir doğru parçasına dönüşüyor (yarı uzunluğu $\sqrt{10}$).

**Cevap:** $\sigma_1 \approx 3.16$, $\sigma_2 = 0$.
