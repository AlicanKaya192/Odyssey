**Ne soruluyor?** İki değişkenli bir fonksiyonun gradyanı ve bir iniş adımının etkisi.

**Fikir:** $\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)$; yeni nokta $p - \eta\nabla f$.

**Adım 1 — $\partial f / \partial x$.** $2xy = 2 \cdot 1 \cdot 2 = 4$.

**Adım 2 — $\partial f / \partial y$.** $x^2 + 3 = 4$.

**Adım 3 — Adım.** Yeni nokta $(1 - 0{,}4; \ 2 - 0{,}4) = (0{,}6; \ 1{,}6)$. $f = 0{,}36 \cdot 1{,}6 + 3 \cdot 1{,}6 = 0{,}576 + 4{,}8 = 5{,}376$.

**Sağlama:** Başlangıçta $f(1, 2) = 2 + 6 = 8$; adım değeri düşürdü ✓. Birinci dereceden tahmin $8 - 0{,}1 \cdot \lVert\nabla f\rVert^2 = 8 - 3{,}2 = 4{,}8$; gerçek düşüş biraz daha az, çünkü fonksiyon eğri.

**Dikkat:** Gradyan yönünde (artı işaretle) gitmek $f$'yi büyütür; iniş için eksi.

**Cevap:** $4$; $4$; $\approx 5{,}376$.
