**Ne soruluyor?** Doğrusal bir modelde kaybın ağırlıklara göre kısmi türevleri ve bir gradyan inişi adımının sonucu.

**Fikir:** Zincir kuralı: $\frac{\partial L}{\partial w_j} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial w_j} = 2(\hat{y} - y) \cdot x_j$.

**Adım 1 — İleri geçiş.** $\hat{y} = 1{,}5$, hata $\hat{y} - y = -1{,}5$, kayıp $2{,}25$.

**Adım 2 — Kısmi türevler.** $\frac{\partial L}{\partial w_1} = 2(-1{,}5)(1) = -3$, $\frac{\partial L}{\partial w_2} = 2(-1{,}5)(2) = -6$, $\frac{\partial L}{\partial b} = -3$.

**Adım 3 — Adım.** $w_1 = 0{,}5 + 0{,}3 = 0{,}8$, $w_2 = 0{,}5 + 0{,}6 = 1{,}1$, $b = 0{,}3$.

**Adım 4 — Yeni kayıp.** $\hat{y} = 0{,}8 + 2{,}2 + 0{,}3 = 3{,}3$; $L = 0{,}3^2 = 0{,}09$.

**Sağlama:** Kayıp $2{,}25$'ten $0{,}09$'a indi ✓. $w_2$, $w_1$'in iki katı kadar değişti: onun özelliği ($x_2 = 2$) iki kat büyük.

**Dikkat:** $b$'yi güncellemeyi unutmak yeni tahmini $3{,}0$ yapardı; bu örnekte tesadüfen kayıp sıfır çıkar ama soru bütün parametrelerin güncellenmesini istiyor.

**Cevap:** $-3$, $-6$ ve $0{,}09$.
