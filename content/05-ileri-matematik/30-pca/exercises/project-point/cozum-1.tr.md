**Ne soruluyor?** Bir noktanın tek bileşene izdüşümü, geri çatılması ve kaybolan kısım.

**Fikir:** $z_1 = u_1^\mathsf{T}(x - \bar{x})$, $\hat{x} = \bar{x} + z_1u_1$.

**Adım 1 — Skor.** $x - \bar{x} = (3, 1)$; $z_1 = \frac{3 + 1}{\sqrt{2}} = 2\sqrt{2} \approx 2{,}828$.

**Adım 2 — Geri çatma.** $z_1u_1 = 2\sqrt{2} \cdot \frac{1}{\sqrt{2}}(1, 1) = (2, 2)$; $\hat{x} = (4, 5)$.

**Adım 3 — Hata.** $x - \hat{x} = (1, -1)$; karesi $2$.

**Sağlama:** Hata vektörü $(1, -1)$, $u_1$'e dik: $(1, -1) \cdot (1, 1) = 0$ ✓.

**Dikkat:** Ortalamayı çıkarmadan $u_1^\mathsf{T}x = \frac{9}{\sqrt{2}}$ almak yanlış skor verir; ortalamayı geri eklemeyi unutmak da $\hat{x}$'i $(2, 2)$ yapar.

**Cevap:** $\approx 2{,}828$; $4$; $2$.
