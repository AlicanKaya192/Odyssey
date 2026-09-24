**Fikir:** Formülü ezberlemeden: her adımda $L$'yi o noktadaki ikinci dereceden Taylor yaklaşımıyla değiştir ve o parabolün dibini bul.

**Adım 1 — $w = 0$'da parabol.** $L(0) = 1$, $L'(0) = -1$, $L''(0) = 1$: $q(\Delta) = 1 - \Delta + \frac{\Delta^2}{2}$. $q'(\Delta) = -1 + \Delta = 0$: $\Delta = 1$, yeni $w = 1$.

**Adım 2 — $w = 1$'de parabol.** $L'(1) = e - 2$, $L''(1) = e$: $q'(\Delta) = (e - 2) + e\Delta = 0$, $\Delta = -\frac{e - 2}{e} \approx -0{,}264$. Yeni $w \approx 0{,}736$.

**Adım 3 — Gerçek dip.** $L'(w) = 0$: $w = \ln 2 \approx 0{,}693$.

**Neden aynı sonuç?** $q(\Delta) = L + L'\Delta + \frac{1}{2}L''\Delta^2$'nin dibi $\Delta = -\frac{L'}{L''}$; Newton formülü bu hesabın kendisi. Parabol gerçek eğriye yakın olduğu ölçüde adım isabetli; ikinci adımda parabol dibe daha yakın kurulduğu için yaklaşım çok daha iyi.

**Cevap:** $1$, $0{,}736$, $0{,}693$.
