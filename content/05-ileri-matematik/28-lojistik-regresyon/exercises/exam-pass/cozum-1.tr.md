**Ne soruluyor?** Bir lojistik modelin iki olasılığı ve karar sınırı.

**Fikir:** $z$'yi hesapla, sigmoide ver; sınır $z = 0$.

**Adım 1 — $x = 2$.** $z = 3 - 4 = -1$. $p = \frac{1}{1 + e^{1}} = \frac{1}{3{,}718} \approx 0{,}269$.

**Adım 2 — $x = 4$.** $z = 6 - 4 = 2$. $p = \frac{1}{1 + e^{-2}} = \frac{1}{1{,}135} \approx 0{,}881$.

**Adım 3 — Sınır.** $1{,}5x - 4 = 0$, $x = \frac{8}{3} \approx 2{,}667$.

**Sağlama:** $2 < 2{,}667 < 4$: birincide olasılık $0{,}5$'in altında, ikincide üstünde ✓.

**Dikkat:** $e^{-z}$'de işaret: $z = -1$ için $e^{-z} = e^{1}$, $e^{-1}$ değil.

**Cevap:** $\approx 0{,}269$; $\approx 0{,}881$; $\approx 2{,}667$.
