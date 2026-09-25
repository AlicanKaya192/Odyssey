**Ne soruluyor?** Aynı veride tam gradyan inişi ile SGD'nin ilk adımları.

**Fikir:** Tam gradyan örnek gradyanlarının ortalaması; SGD her adımda tek bir örneğin gradyanını kullanır ve bir sonraki adıma güncellenmiş $w$ ile geçer.

**Adım 1 — Örnek gradyanları.** $w = 0$: $\ell_1' = -2 \cdot 1 \cdot 2 = -4$, $\ell_2' = -2 \cdot 3 \cdot 3 = -18$. Ortalama $-11$.

**Adım 2 — Tam adım.** $w = 0 - 0{,}05 \cdot (-11) = 0{,}55$.

**Adım 3 — SGD, ikinci örnek.** $w = 0 - 0{,}05 \cdot (-18) = 0{,}9$.

**Adım 4 — SGD, birinci örnek.** $\ell_1'(0{,}9) = -2 \cdot 1 \cdot (2 - 0{,}9) = -2{,}2$: $w = 0{,}9 + 0{,}11 = 1{,}01$.

**Sağlama:** En iyi $w$ (ortalama kayıp için) $\frac{\sum x_i y_i}{\sum x_i^2} = \frac{11}{10} = 1{,}1$. İki SGD adımı ($1{,}01$) tek tam adımdan ($0{,}55$) daha yakın; ama SGD iki kez gradyan hesapladı ve adımları gürültülü.

**Dikkat:** SGD'nin ikinci adımında gradyanı hâlâ $w = 0$'da hesaplamak ($-4$ ile) $w = 1{,}1$ verir; tesadüfen en iyi değer, ama yöntem yanlış.

**Cevap:** $-11$, $0{,}55$ ve $1{,}01$.
