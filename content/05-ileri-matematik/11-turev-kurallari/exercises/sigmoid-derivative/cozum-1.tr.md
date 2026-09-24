**Ne soruluyor?** Sigmoidin türevinin iki noktadaki değeri ve dört katmanda biriken çarpım.

**Fikir:** $\sigma' = \sigma(1 - \sigma)$ biçimi, türevi $\sigma$'nın değerinden okumayı sağlar: önce $\sigma$'yı bul, sonra $\sigma(1 - \sigma)$.

**Adım 1 — $x = 0$.** $\sigma(0) = \frac{1}{2}$: $\sigma'(0) = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$.

**Adım 2 — $x = \ln 3$.** $e^{-\ln 3} = \frac{1}{3}$, $\sigma(\ln 3) = \frac{1}{4/3} = \frac{3}{4}$: $\sigma' = \frac{3}{4} \cdot \frac{1}{4} = \frac{3}{16}$.

**Adım 3 — Dört katman.** $\left(\frac{1}{4}\right)^4 = \frac{1}{256} \approx 0{,}0039$.

**Sağlama:** $\frac{3}{16} = 0{,}1875 < 0{,}25$: $\sigma'$ en büyük değerini $0$'da alır, başka her yerde daha küçük ✓.

**Dikkat:** Bu en iyimser durum. Nöronların çoğu $0$'dan uzakta çalışırsa çarpanlar $0{,}1$'in altına düşer ve dört katmanda gradyan on binde birin altına iner.

**Cevap:** $\frac{1}{4}$, $\frac{3}{16}$ ve $\frac{1}{256}$.
