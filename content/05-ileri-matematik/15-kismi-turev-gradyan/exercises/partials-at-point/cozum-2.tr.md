**Fikir:** Kısmi türevin geometrisini doğrudan kullan: sabit tutulacak değişkeni hemen yerine koy, tek değişkenli bir fonksiyon kalsın, onun türevini al.

**Adım 1 — $y = 2$ kesiti.** $g(x) = f(x, 2) = 4x^3 - 8x + 8$. $g'(x) = 12x^2 - 8$, $g'(1) = 4$.

**Adım 2 — $x = 1$ kesiti.** $h(y) = f(1, y) = y^2 - 4y + y^3$. $h'(y) = 2y - 4 + 3y^2$, $h'(2) = 4 - 4 + 12 = 12$.

**Neden aynı sonuç?** $\frac{\partial f}{\partial x}(1, 2)$, yüzeyin $y = 2$ düzlemiyle kesitinin $x = 1$'deki eğimi; $g$ tam o kesit. Tek bir noktada kısmi türev isteniyorsa bu yol daha az harfle çalışıyor.

**Cevap:** $4$ ve $12$.
