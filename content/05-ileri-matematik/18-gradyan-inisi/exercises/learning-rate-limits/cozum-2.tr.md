**Fikir:** $w_0 = 1$'den başlayıp birkaç adım at; davranış çarpanı doğrudan gösterir.

**Adım 1 — $\eta = 0{,}3$.** $L'(1) = 6$: $w_1 = 1 - 1{,}8 = -0{,}8$. $L'(-0{,}8) = -4{,}8$: $w_2 = -0{,}8 + 1{,}44 = 0{,}64$. Oran $\frac{w_1}{w_0} = -0{,}8$.

**Adım 2 — $\eta = \frac{1}{6}$.** $w_1 = 1 - \frac{6}{6} = 0$: tek adımda dip.

**Adım 3 — Sınırı bul.** Oranın büyüklüğü $1$'i geçmemeli: $6\eta - 1 < 1$, $\eta < \frac{1}{3}$.

**Neden aynı sonuç?** Birkaç adım, $w_{k+1} = (1 - 6\eta)w_k$ kuralının sayısal görüntüsü. İkinci türevin en iyi adımı söylemesi ($\eta = \frac{1}{L''}$) Newton yönteminin tek değişkenli hâli: parabolde tam adım.

**Cevap:** $\frac{1}{3}$, $-0{,}8$, $\frac{1}{6}$.
