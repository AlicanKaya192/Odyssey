**Fikir:** Laplace düzeltmesi, gerçek veriden önce her sınıfa iki sahte e-posta eklemektir: birinde kelime var, birinde yok. Sonra düz MLE alınır.

**Adım 1 — Sahte gözlemsiz.** Spam: $40$ e-postada $0$ kez, oran $0$.

**Adım 2 — Spam.** $42$ e-postada $1$ kez: $\frac{1}{42} \approx 0{,}0238$.

**Adım 3 — Normal.** $62$ e-postada $13$ kez: $\frac{13}{62} \approx 0{,}210$.

**Neden aynı sonuç?** $\frac{k + 1}{n + 2}$, veriye $1$ "var" ve $1$ "yok" eklenmiş hâlin gözlenen oranıdır. Bayes diliyle bu, her $p$ değerini eşit olası sayan (düzgün) bir önselle bulunan sonsalın beklenen değeri; sahte gözlemler önsel inancın veri kılığı.

**Cevap:** $0$; $0{,}0238$ ve $0{,}210$.
