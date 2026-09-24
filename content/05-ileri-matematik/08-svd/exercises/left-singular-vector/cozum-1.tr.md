**Ne soruluyor?** Çemberdeki $\mathbf{v}_1$ noktasının $A$ ile gittiği yön: elipsin en uzun ekseninin doğrultusu.

**Fikir:** SVD'nin temel ilişkisi $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$. $A\mathbf{v}_1$'i hesaplayıp $\sigma_1$'e bölersek $\mathbf{u}_1$ çıkar.

**Adım 1 — $A\mathbf{v}_1$.** $\tfrac{1}{\sqrt{2}}$ çarpanını dışarıda bırakalım:

$$
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 4 + 5 \end{bmatrix} = \begin{bmatrix} 3 \\ 9 \end{bmatrix}
$$

Öyleyse $A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(3, 9)$.

**Adım 2 — $\sigma_1$'e böl.** $\sigma_1 = 3\sqrt{5}$:

$$
\begin{aligned}
\mathbf{u}_1 &= \frac{1}{3\sqrt{5}} \cdot \frac{1}{\sqrt{2}} \begin{bmatrix} 3 \\ 9 \end{bmatrix} \\
&= \frac{1}{\sqrt{10}} \begin{bmatrix} 1 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Adım 3 — Sayıya çevir.** $\sqrt{10} \approx 3.162$:

$$
\mathbf{u}_1 \approx (0.316,\ 0.949)
$$

**Sağlama:** Birim vektör mü? $\tfrac{1}{10}(1 + 9) = 1$ ✓. $A\mathbf{v}_1$'in uzunluğu gerçekten $\sigma_1$ mi? $\tfrac{1}{\sqrt{2}}\sqrt{9 + 81} = \tfrac{\sqrt{90}}{\sqrt{2}} = \sqrt{45} = 3\sqrt{5}$ ✓.

**Sonucu yorumla:** Elipsin en uzun ekseni $(1, 3)$ doğrultusunda, yani yataydan yaklaşık $72°$ yukarıda. Girdi yönü $\mathbf{v}_1$ ise $45°$'deydi: $A$ bu yönü hem döndürüp hem uzattı.

**Cevap:** $\mathbf{u}_1 \approx (0.32,\ 0.95)$.
