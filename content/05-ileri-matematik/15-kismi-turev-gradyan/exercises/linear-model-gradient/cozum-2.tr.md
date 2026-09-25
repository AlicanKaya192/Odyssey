**Fikir:** Parametreleri tek vektörde topla: $\boldsymbol{\theta} = (w_1, w_2, b)$, girdi de $(x_1, x_2, 1)$. Gradyan tek satırda: $\nabla L = 2(\hat{y} - y)(x_1, x_2, 1)$.

**Adım 1 — Gradyan.** $2(-1{,}5)(1, 2, 1) = (-3, -6, -3)$.

**Adım 2 — Adım.** $\boldsymbol{\theta} \leftarrow (0{,}5; 0{,}5; 0) - 0{,}1 \cdot (-3, -6, -3) = (0{,}8; 1{,}1; 0{,}3)$.

**Adım 3 — Kayıp.** $\hat{y} = (0{,}8; 1{,}1; 0{,}3) \cdot (1, 2, 1) = 3{,}3$, $L = 0{,}09$.

**Neden aynı sonuç?** Aynı üç kısmi türev, bir vektörün bileşenleri olarak yazıldı. Bu yazımın gücü: $10$ ya da $10$ milyon ağırlık olsa da formül aynı satır. Kütüphaneler gradyanı tam böyle, bir vektör işlemi olarak hesaplıyor.

**Cevap:** $-3$, $-6$, $0{,}09$.
