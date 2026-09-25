**Fikir:** $f$ yalnızca $u = x + 2y$'ye bağlı: $f = e^u$. Noktada $u = 0{,}1 + 0{,}1 = 0{,}2$. Tek değişkenli Taylor yeter.

**Adım 1 — Doğrusal.** $e^u \approx 1 + u = 1{,}2$.

**Adım 2 — İkinci derece.** $e^u \approx 1 + u + \frac{u^2}{2} = 1 + 0{,}2 + 0{,}02 = 1{,}22$.

**Neden aynı sonuç?** $\nabla f \cdot \mathbf{h} = (1, 2) \cdot \mathbf{h} = u$ ve $\mathbf{h}^\mathsf{T} H \mathbf{h} = \mathbf{h}^\mathsf{T} \begin{bmatrix} 1 \\ 2 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix} \mathbf{h} = u^2$. Hessian burada rank-1 bir matris: fonksiyon yalnızca tek bir yönde ($(1, 2)$ yönünde) kıvrılıyor, ona dik yönde düz.

**Cevap:** $1{,}2$ ve $1{,}22$.
