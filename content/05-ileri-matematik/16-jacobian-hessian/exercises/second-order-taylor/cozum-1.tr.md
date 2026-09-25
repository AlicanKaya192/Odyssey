**Ne soruluyor?** İki değişkenli bir fonksiyonun birinci ve ikinci dereceden Taylor yaklaşımları.

**Fikir:** $f(\mathbf{p} + \mathbf{h}) \approx f + \nabla f \cdot \mathbf{h} + \frac{1}{2}\mathbf{h}^\mathsf{T} H \mathbf{h}$.

**Adım 1 — Türevler.** $f_x = e^{x + 2y}$, $f_y = 2e^{x + 2y}$; $f_{xx}$, $f_{xy}$, $f_{yy}$ sırasıyla $e^{x + 2y}$'nin $1$, $2$ ve $4$ katı. $(0, 0)$'da $\nabla f = (1, 2)$, $H = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$.

**Adım 2 — Doğrusal.** $1 + (1, 2) \cdot (0{,}1; 0{,}05) = 1 + 0{,}1 + 0{,}1 = 1{,}2$.

**Adım 3 — Hessian terimi.** $H\mathbf{h} = (0{,}1 + 0{,}1; \ 0{,}2 + 0{,}2) = (0{,}2; 0{,}4)$; $\mathbf{h}^\mathsf{T} H \mathbf{h} = 0{,}02 + 0{,}02 = 0{,}04$; yarısı $0{,}02$. Toplam $1{,}22$.

**Sağlama:** Gerçek değer $e^{0{,}2} \approx 1{,}2214$. Hata doğrusal yaklaşımda $0{,}021$, ikinci derecede $0{,}0014$ ✓.

**Dikkat:** $\frac{1}{2}$'yi unutmak ikinci terimi $0{,}04$ yapar ve sonuç $1{,}24$ çıkar; gerçeği aşar.

**Cevap:** $1{,}2$ ve $1{,}22$.
