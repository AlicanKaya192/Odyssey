**Ne soruluyor?** Bir oranın MLE'si, o noktadaki log-olabilirlik ve başka bir noktadaki eğim.

**Fikir:** $\ell'(p) = 0$ en büyük noktayı verir; başka bir noktada türevin işareti, en büyüğün hangi yanda olduğunu söyler.

**Adım 1 — MLE.** $\frac{8}{p} = \frac{192}{1 - p}$, $8(1 - p) = 192p$, $\hat{p} = \frac{8}{200} = 0{,}04$.

**Adım 2 — $\ell(\hat{p})$.** $8 \cdot (-3{,}2189) + 192 \cdot (-0{,}0408) \approx -25{,}75 - 7{,}84 = -33{,}59$.

**Adım 3 — $\ell'(0{,}05)$.**

$$
\frac{8}{0{,}05} - \frac{192}{0{,}95} = 160 - 202{,}11 \approx -42{,}11
$$

Negatif: $p = 0{,}05$'te log-olabilirlik azalıyor; en büyük nokta daha solda, yani $0{,}05$'ten küçük.

**Sağlama:** $\ell'(0{,}04) = 200 - 200 = 0$ ✓.

**Dikkat:** $\ln(1 - p)$'nin türevi $-\frac{1}{1 - p}$; eksi işareti unutulursa denklem çözümsüz kalır.

**Cevap:** $0{,}04$; $\approx -33{,}59$; $\approx -42{,}11$.
