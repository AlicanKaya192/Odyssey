**Fikir:** En iyi nokta $w^* = 4$. Uzaklık $d = w - 4$ olsun; bir adım $d$'yi sabit bir sayıyla çarpar.

**Adım 1 — Çarpan.** $w - 0{,}25 \cdot 2(w - 4) - 4 = (w - 4)(1 - 0{,}5)$: $d \leftarrow 0{,}5 \, d$.

**Adım 2 — Uzaklıklar.** $d_0 = -4$, $d_1 = -2$, $d_2 = -1$, $d_3 = -0{,}5$.

**Adım 3 — Geri çevir.** $w = 4 + d$: $2$, $3$, $3{,}5$.

**Neden aynı sonuç?** Karesel kayıpta gradyan inişi uzaklığı her adımda $1 - \eta\lambda$ ile çarpar; burada $\lambda = L'' = 2$, $1 - 0{,}5 = 0{,}5$. Bu bakış, kaç adımda nereye varılacağını tek formülle veriyor: $w_k = 4 - 4 \cdot 0{,}5^k$.

**Cevap:** $2$, $3$, $3{,}5$.
