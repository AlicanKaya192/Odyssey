**Fikir:** Yanlış alarm sayısı $X$, $n = 20$ ve $p = 0{,}05$ ile bir binom değişkeni.

**Adım 1 — Beklenen değer.** $E[X] = np = 1$.

**Adım 2 — En az bir.** $P(X \geq 1) = 1 - P(X = 0) = 1 - \binom{20}{0} 0{,}05^0 \, 0{,}95^{20} \approx 0{,}642$.

**Adım 3 — Eşik.** Toplam yanlış alarm olasılığını en fazla $0{,}05$ tutmak için $P(X \geq 1) \leq 20 \alpha' \leq 0{,}05$ yeterli; $\alpha' = 0{,}0025$.

**Neden aynı sonuç?** Binomun $P(X = 0)$ terimi, "hiçbir test yanlış alarm vermez" olayının olasılığıdır; birinci yoldaki çarpım aynı sayı.

**Cevap:** $1$; $0{,}642$ ve $0{,}0025$.
