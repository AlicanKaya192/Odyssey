**Ne soruluyor?** İki fonksiyonu sürekli yapan parametre değerleri.

**Fikir:** Süreklilik: $f(a)$ tanımlı, limit var, ikisi eşit. Parçaların içinde sorun yok; yalnızca birleşme noktasını kontrol et.

**Adım 1 — $f$ için sol limit.** $x \to 2^-$: $x^2 + a \to 4 + a$.

**Adım 2 — $f$ için sağ limit ve değer.** $x \to 2^+$ ve $f(2)$: $3 \cdot 2 - 1 = 5$.

**Adım 3 — Eşitle.** $4 + a = 5$, $a = 1$.

**Adım 4 — $g$ için limit.** $\frac{(x - 2)(x + 2)}{x - 2} = x + 2 \to 4$. Değer limite eşit olmalı: $k = 4$.

**Sağlama:** $a = 1$: solda $x = 1{,}99$ için $1{,}99^2 + 1 = 4{,}9601$, sağda $x = 2{,}01$ için $5{,}03$. İkisi de $5$'e yakın ✓.

**Dikkat:** $g(2)$'yi formülden hesaplamaya çalışmak $\frac{0}{0}$ verir; $g(2)$ formülle değil, $k$ ile tanımlı.

**Cevap:** $a = 1$, $k = 4$.
