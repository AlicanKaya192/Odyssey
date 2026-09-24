**Ne soruluyor?** Sorguya hangi belge daha çok benziyor? Benzerliği kelime sayılarının büyüklüğüyle değil, **yönüyle** ölçeceğiz: iki vektör aynı yöne bakıyorsa aynı konudan bahsediyor demektir.

**Fikir:** Kosinüs benzerliği, iki vektör arasındaki açının kosinüsü:

$$
\cos(\mathbf{q}, D) = \frac{\mathbf{q} \cdot D}{\|\mathbf{q}\|\,\|D\|}
$$

Nokta çarpımını uzunluklara bölmek, belgenin ne kadar uzun olduğunu hesaptan çıkarıyor. Sonuç $1$'e ne kadar yakınsa yönler o kadar aynı.

**Adım 1 — Nokta çarpımları.** Karşılıklı bileşenleri çarpıp topla:

$$
\begin{aligned}
\mathbf{q} \cdot D_1 &= 1 \cdot 2 + 1 \cdot 2 + 0 \cdot 1 = 4 \\
\mathbf{q} \cdot D_2 &= 1 \cdot 0 + 1 \cdot 6 + 0 \cdot 8 = 6
\end{aligned}
$$

**Adım 2 — Uzunluklar.**

$$
\begin{aligned}
\|\mathbf{q}\| &= \sqrt{1 + 1 + 0} = \sqrt{2} \\
\|D_1\| &= \sqrt{4 + 4 + 1} = \sqrt{9} = 3 \\
\|D_2\| &= \sqrt{0 + 36 + 64} = \sqrt{100} = 10
\end{aligned}
$$

**Adım 3 — Kosinüsler.** $\sqrt{2} \approx 1.414$:

$$
\begin{aligned}
\cos(\mathbf{q}, D_1) &= \frac{4}{\sqrt{2} \cdot 3} \approx \frac{4}{4.243} \approx 0.94 \\
\cos(\mathbf{q}, D_2) &= \frac{6}{\sqrt{2} \cdot 10} \approx \frac{6}{14.14} \approx 0.42
\end{aligned}
$$

**Sonucu yorumla:** Düz nokta çarpımına bakılsaydı $D_2$ ($6 > 4$) daha benzer görünürdü. Oysa $D_2$ çoğunlukla *olasılık* üzerine; sayıları yalnızca uzun bir belge olduğu için büyük. Kosinüs uzunluğu bölerek atınca, sorguyla aynı konuyu (*vektör* ve *matris*) anlatan $D_1$ açık ara öne geçiyor.

**Dikkat:** Uzunluğa bölmeyi unutursan uzun belgeler her aramada öne çıkar.

**Cevap:** $0.94$ ve $0.42$; $D_1$ daha benzer.
