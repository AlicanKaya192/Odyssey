**Fikir:** Yönlü türevin tanımına dön: $(2, 1)$'den $\mathbf{u}$ yönünde $t$ kadar yürü, yüksekliği $t$'nin fonksiyonu olarak yaz ve $t = 0$'da türevini al.

**Adım 1 — Yol.** $x = 2 + 0{,}6t$, $y = 1 + 0{,}8t$.

**Adım 2 — Yükseklik.** $g(t) = (2 + 0{,}6t)^2 + 3(1 + 0{,}8t)^2$.

**Adım 3 — Türev.** $g'(t) = 2(2 + 0{,}6t)(0{,}6) + 6(1 + 0{,}8t)(0{,}8)$; $g'(0) = 2{,}4 + 4{,}8 = 7{,}2$.

**Neden aynı sonuç?** $g'(0)$'daki iki terim, $f_x \cdot u_1 = 4 \cdot 0{,}6$ ve $f_y \cdot u_2 = 6 \cdot 0{,}8$: zincir kuralı nokta çarpımını kendiliğinden üretiyor. $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$ formülünün kanıtı da tam olarak bu. Gradyan bileşenleri de $\mathbf{u} = (1, 0)$ ve $(0, 1)$ yönlerindeki yönlü türevler: $4$ ve $6$.

**Cevap:** $4$, $6$, $7{,}2$.
