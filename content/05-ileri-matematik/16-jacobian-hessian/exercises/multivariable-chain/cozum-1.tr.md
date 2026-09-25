**Ne soruluyor?** İki ara değişken üzerinden $t$'ye bağlı bir büyüklüğün değişim hızı.

**Fikir:** $t$ değişince $z$ hem $x$ hem $y$ üzerinden etkilenir; her yolun katkısı kısmi türev çarpı ara değişkenin türevi.

**Adım 1 — Değerler.** $t = 1$: $x = 2$, $y = 2$.

**Adım 2 — Kısmi türevler.** $z_x = 2xy = 8$, $z_y = x^2 = 4$.

**Adım 3 — Topla.** $\frac{dz}{dt} = 8 \cdot 2 + 4 \cdot 2 = 24$.

**Sağlama:** $x$ yolunun katkısı $16$, $y$ yolununki $8$. $z$'yi $t$'ye göre sayısal olarak kontrol et: $z(1{,}01) = (2{,}02)^2 (2{,}0201) \approx 8{,}2426$, $z(1) = 8$; fark bölü $0{,}01 \approx 24{,}3$ ✓.

**Dikkat:** Yalnızca bir yolu almak ($16$ ya da $8$) yanlış; bağımlılık iki yoldan geliyor.

**Cevap:** $24$ ve $8$.
