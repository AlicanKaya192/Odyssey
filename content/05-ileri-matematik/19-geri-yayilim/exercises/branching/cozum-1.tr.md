**Ne soruluyor?** İki girdinin iki ayrı ara değerden geçerek çıktıyı etkilediği bir grafikte türevler.

**Fikir:** Her girdinin gradyanı, çıktıya giden bütün yolların katkılarının toplamı.

**Adım 1 — İleri.** $s = 4$, $d = 2$, $g = 8$.

**Adım 2 — Çarpma.** $\frac{\partial g}{\partial s} = d = 2$, $\frac{\partial g}{\partial d} = s = 4$.

**Adım 3 — $x$.** $s$ yolundan $2 \cdot 1$, $d$ yolundan $4 \cdot 1$: toplam $6$.

**Adım 4 — $y$.** $s$ yolundan $2 \cdot 1$, $d$ yolundan $4 \cdot (-1)$: toplam $-2$.

**Sağlama:** Çıkarma düğümü gradyanın işaretini ikinci girdiye ters çeviriyor ($a - b$ için $g$, $-g$) ✓.

**Dikkat:** Tek bir yoldan hesaplamak $\frac{\partial g}{\partial x}$'i $2$ ya da $4$ bulur; ikisi de eksik.

**Cevap:** $6$ ve $-2$.
