**Ne soruluyor?** Tek tek ve ortalama log-loss, ve emin olup yanlış olmanın bedeli.

**Fikir:** Her örnekte doğru sınıfa verilen olasılığın eksi logaritması.

**Adım 1 — Üçüncü.** $y = 1$, $-\ln 0{,}4 \approx 0{,}916$.

**Adım 2 — Ortalama.** Birinci $-\ln 0{,}9 \approx 0{,}105$; ikinci $y = 0$, $-\ln 0{,}8 \approx 0{,}223$. Toplam $1{,}245$; ortalama $\approx 0{,}415$.

**Adım 3 — $p_3 = 0{,}01$.** $-\ln 0{,}01 \approx 4{,}605$: tek başına öteki iki örneğin toplamının on katından fazla.

**Sağlama:** Doğru sınıfa en yüksek olasılığı veren birinci örnek ($0{,}9$) en küçük kaybı alıyor ✓.

**Dikkat:** İkinci örnekte $-\ln 0{,}2$ almak; $y = 0$ olduğu için doğru sınıfın olasılığı $1 - 0{,}2 = 0{,}8$.

**Cevap:** $\approx 0{,}916$; $\approx 0{,}415$; $\approx 4{,}605$.
