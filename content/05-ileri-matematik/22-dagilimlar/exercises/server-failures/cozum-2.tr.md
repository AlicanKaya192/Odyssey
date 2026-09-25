**Fikir:** $t$ saatte hiç arıza olmaması, o süredeki arıza sayısının $0$ olması. Arıza sayısı Poisson$(\frac{t}{200})$.

**Adım 1 — Ortalama.** Saatte $\frac{1}{200}$ arıza; iki arıza arası ortalama $200$ saat.

**Adım 2 — $100$ saat.** $100$ saatte beklenen arıza $0{,}5$; Poisson'da $P(0) = e^{-0{,}5} \approx 0{,}6065$.

**Adım 3 — Ortanca.** $P(0) = e^{-t/200} = \frac{1}{2}$, $t = 200 \ln 2$.

**Neden aynı sonuç?** "Bekleme $t$'den uzun" ile "$t$ süresinde sıfır olay" aynı olay; üstel dağılım, Poisson süreçlerinin bekleme süresi.

**Cevap:** $200$; $0{,}6065$ ve $138{,}63$.
