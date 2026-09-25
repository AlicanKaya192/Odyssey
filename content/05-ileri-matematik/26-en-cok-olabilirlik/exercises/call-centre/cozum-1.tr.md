**Ne soruluyor?** Poisson parametresinin MLE'si, onunla bir olasılık ve başka bir noktada eğim.

**Fikir:** $\ell'(\lambda) = \frac{\sum x_i}{\lambda} - n$.

**Adım 1 — MLE.** $\sum x_i = 24$, $n = 6$. $\frac{24}{\lambda} = 6$, $\hat{\lambda} = 4$.

**Adım 2 — Hiç çağrı yok.** $P(X = 0) = \frac{4^0 e^{-4}}{0!} = e^{-4} \approx 0{,}0183$.

**Adım 3 — $\ell'(5)$.** $\frac{24}{5} - 6 = -1{,}2$. Negatif: $5$ fazla büyük, en büyük nokta solda.

**Sağlama:** $\ell''(\lambda) = -\frac{24}{\lambda^2} < 0$; $\hat{\lambda} = 4$ gerçekten en büyük ✓.

**Dikkat:** Log-olabilirlikteki $\ln x_i!$ terimleri $\lambda$'ya bağlı değil; türevde kaybolurlar.

**Cevap:** $4$; $\approx 0{,}0183$; $-1{,}2$.
