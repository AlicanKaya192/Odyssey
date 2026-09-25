**Ne soruluyor?** Hatalı ürünün toplam olasılığı ve hatalı ürünün hangi makineden geldiğinin sonsal olasılıkları.

**Fikir:** Makineler örnek uzayı üç parçaya böler. Toplam olasılık kuralı $P(\text{hatalı})$'yı, Bayes kuralı sonsalları verir.

**Adım 1 — Paylar.** A: $0{,}5 \cdot 0{,}02 = 0{,}010$; B: $0{,}3 \cdot 0{,}03 = 0{,}009$; C: $0{,}2 \cdot 0{,}05 = 0{,}010$. Toplam $0{,}029$.

**Adım 2 — C.** $P(C \mid \text{hatalı}) = \frac{0{,}010}{0{,}029} \approx 0{,}345$.

**Adım 3 — B.** $P(B \mid \text{hatalı}) = \frac{0{,}009}{0{,}029} \approx 0{,}310$.

**Sağlama:** A da $\frac{0{,}010}{0{,}029} \approx 0{,}345$; üçü toplam $0{,}345 + 0{,}310 + 0{,}345 = 1$ ✓.

**Dikkat:** C'nin sonsalını hata oranı ($0{,}05$) ya da üretim payı ($0{,}2$) sanmak; sonsal ikisinin çarpımının toplam içindeki payı.

**Cevap:** $0{,}029$; $\approx 0{,}345$; $\approx 0{,}310$.
