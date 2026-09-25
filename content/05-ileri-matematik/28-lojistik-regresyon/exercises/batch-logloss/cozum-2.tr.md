**Fikir:** Toplam log-loss, doğru sınıf olasılıklarının çarpımının (olabilirliğin) eksi logaritmasıdır.

**Adım 1 — Üçüncü.** Doğru sınıf olasılığı $0{,}4$; $-\ln 0{,}4 \approx 0{,}916$.

**Adım 2 — Çarpım.** $L = 0{,}9 \cdot 0{,}8 \cdot 0{,}4 = 0{,}288$. $-\ln 0{,}288 \approx 1{,}245$; $3$'e bölünce $0{,}415$.

**Adım 3 — $p_3 = 0{,}01$.** Olabilirlik $0{,}9 \cdot 0{,}8 \cdot 0{,}01 = 0{,}0072$'ye düşer; üçüncü örneğin payı $-\ln 0{,}01 \approx 4{,}605$.

**Neden aynı sonuç?** $-\ln(abc) = -\ln a - \ln b - \ln c$; log-loss, olabilirliği toplamlara bölmenin ta kendisi. Tek bir olasılık sıfıra yaklaşınca bütün çarpım çöker; logaritmada bu, tek bir terimin patlaması olarak görünür.

**Cevap:** $0{,}916$; $0{,}415$ ve $4{,}605$.
