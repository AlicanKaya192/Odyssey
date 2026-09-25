**Ne soruluyor?** Aynı puanlardan softmax ve sigmoid olasılıkları, bir de sınıf eklenince olasılığın nasıl değiştiği.

**Fikir:** Softmax, her sınıfın $e^{z}$ değerini toplama böler. Sigmoid için üs kurallarıyla $e^{-(z_1 - z_2)}$ verilen sayılardan bulunur.

**Adım 1 — İki sınıflı softmax.**

$$
p_1 = \frac{12}{12 + 4} = \frac{12}{16} = \frac{3}{4}
$$

**Adım 2 — Sigmoid.** $e^{-(z_1 - z_2)} = e^{z_2 - z_1} = \frac{e^{z_2}}{e^{z_1}} = \frac{4}{12} = \frac{1}{3}$.

$$
\sigma(z_1 - z_2) = \frac{1}{1 + \frac{1}{3}} = \frac{1}{\frac{4}{3}} = \frac{3}{4}
$$

**Adım 3 — Üç sınıf.**

$$
p_1 = \frac{12}{12 + 4 + 4} = \frac{12}{20} = \frac{3}{5}
$$

**Sağlama:** Üç sınıfta olasılıklar $\frac{12}{20}, \frac{4}{20}, \frac{4}{20}$; toplam $1$ ✓.

**Dikkat:** Yeni sınıf eklenince birinci sınıfın puanı değişmediği hâlde olasılığı düşüyor: softmax olasılıkları birbirine bağlı, payda bütün sınıfları içeriyor.

**Cevap:** $\frac{3}{4}$, $\frac{3}{4}$, $\frac{3}{5}$.
