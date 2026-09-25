**Ne soruluyor?** İki değişkenli bir fonksiyonda iki gradyan inişi adımı.

**Fikir:** Her adımda gradyanı hesapla ve iki koordinatı birlikte güncelle.

**Adım 1.** $\nabla f(2, 1) = (4, 8)$: $(2 - 0{,}4; \ 1 - 0{,}8) = (1{,}6; \ 0{,}2)$.

**Adım 2.** $\nabla f(1{,}6; 0{,}2) = (3{,}2; \ 1{,}6)$: $(1{,}6 - 0{,}32; \ 0{,}2 - 0{,}16) = (1{,}28; \ 0{,}04)$.

**Adım 3 — Değer.** $f = 1{,}28^2 + 4 \cdot 0{,}04^2 = 1{,}6384 + 0{,}0064 = 1{,}6448$.

**Sağlama:** Başlangıçta $f = 4 + 4 = 8$; iki adımda $1{,}64$'e indi ✓. $y$ hızla sıfıra yaklaştı, $x$ yavaş: kayıp artık neredeyse tamamen $x$'ten geliyor.

**Dikkat:** İki koordinat aynı anda güncellenir; ikinci koordinatın gradyanını, birinci güncellendikten sonraki değerle hesaplamak başka bir yöntem olur.

**Cevap:** $(1{,}6; 0{,}2)$ ve $f \approx 1{,}6448$.
