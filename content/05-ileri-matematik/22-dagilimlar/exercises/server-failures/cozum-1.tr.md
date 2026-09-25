**Ne soruluyor?** Üstel bekleme süresinin ortalaması, bir kuyruk olasılığı ve ortancası.

**Fikir:** $P(X > t) = e^{-\lambda t}$, $E[X] = \frac{1}{\lambda}$.

**Adım 1 — Ortalama.** $\frac{1}{1/200} = 200$ saat.

**Adım 2 — $100$ saat.** $e^{-100/200} = e^{-0{,}5} \approx 0{,}6065$.

**Adım 3 — Ortanca.** $e^{-t/200} = 0{,}5$, $-\frac{t}{200} = \ln 0{,}5 = -\ln 2$, $t = 200 \ln 2 \approx 138{,}63$ saat.

**Sağlama:** Ortanca ortalamadan küçük ($138{,}63 < 200$): üstel dağılım sağa çarpık, uzun beklemeler ortalamayı yukarı çekiyor ✓.

**Dikkat:** "Ortalama $200$ saat" dediği için yarı olasılığın $200$'de dolduğunu sanmak; $P(X > 200) = e^{-1} \approx 0{,}37$.

**Cevap:** $200$; $\approx 0{,}6065$; $\approx 138{,}63$.
