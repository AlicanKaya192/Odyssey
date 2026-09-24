**Ne soruluyor?** İki veri noktasından modelin iki parametresini bulmak ve modeli kullanmak.

**Fikir:** Model bir noktadan geçiyorsa o noktanın $x$'ini koyunca $y$'sini vermeli. Her nokta $w$ ve $b$ için bir denklem; iki nokta, iki bilinmeyen.

**Adım 1 — Denklemler.**

$$
\begin{cases}
2w + b = 7 \\
5w + b = 16
\end{cases}
$$

**Adım 2 — Çıkar.** $b$'nin katsayıları aynı:

$$
3w = 9 \quad\Rightarrow\quad w = 3
$$

**Adım 3 — $b$.** $2 \cdot 3 + b = 7$, $b = 1$. Model $\hat{y} = 3x + 1$.

**Adım 4 — Tahmin.** $\hat{y} = 3 \cdot 10 + 1 = 31$.

**Sağlama:** $3 \cdot 2 + 1 = 7$ ✓, $3 \cdot 5 + 1 = 16$ ✓.

**Sonucu yorumla:** $w = 3$, "$x$ bir artınca tahmin $3$ artıyor" demek; $b = 1$, $x = 0$'daki tahmin. Yalnızca iki noktayla kurulan bir model veriyi tam ezberler; gerçek veride nokta çok olduğu için regresyon hatayı en küçük yapan doğruyu arar.

**Cevap:** $w = 3$, $b = 1$; tahmin $31$.
