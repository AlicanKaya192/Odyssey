**Fikir:** Olabilirliği logaritmayla toplamaya çevir; lojistik regresyonun kaybı tam olarak bunun eksisi.

**Adım 1 — Log-olabilirlik.** $\ln 0{,}8 + \ln 0{,}4 + \ln 0{,}9 \approx -0{,}2231 - 0{,}9163 - 0{,}1054 = -1{,}2448$. $e^{-1{,}2448} \approx 0{,}288$.

**Adım 2 — Beklenen değer.** Doğrusallık: $\sum p_i = 2{,}3$.

**Adım 3 — Varyans.** $\sum p_i(1 - p_i) = 0{,}49$.

**Neden aynı sonuç?** Çarpımın logaritması logaritmaların toplamı; log-kayıp ($1{,}2448 / 3 \approx 0{,}415$ örnek başına) bu toplamın eksisinin ortalaması. En Çok Olabilirlik bölümü bu bağlantıyı genelleştiriyor.

**Cevap:** $0{,}288$; $2{,}3$ ve $0{,}49$.
