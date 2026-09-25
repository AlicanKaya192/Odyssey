**Ne soruluyor?** Softmax olasılıkları, çapraz entropi ve doğru sınıfın skoruna göre gradyan.

**Fikir:** Üstel al, topla, böl; kayıp doğru sınıfın olasılığının eksi logaritması.

**Adım 1 — Olasılıklar.** Toplam $7{,}389 + 2{,}718 + 1{,}105 = 11{,}212$. $p_1 = \frac{7{,}389}{11{,}212} \approx 0{,}659$, $p_2 \approx 0{,}242$, $p_3 \approx 0{,}099$.

**Adım 2 — Kayıp.** $-\ln 0{,}242 \approx 1{,}417$.

**Adım 3 — Türev.** $p_2 - 1 \approx -0{,}758$: $z_2$'yi artırmak kaybı azaltır.

**Sağlama:** Olasılıkların toplamı $0{,}659 + 0{,}242 + 0{,}099 = 1$ ✓.

**Dikkat:** Kayıp en büyük olasılıktan ($p_1$) değil, doğru sınıfın olasılığından hesaplanır; model yanlış sınıfa en yüksek olasılığı verdiği için kayıp büyük.

**Cevap:** $\approx 0{,}659$; $\approx 1{,}417$; $\approx -0{,}758$.
