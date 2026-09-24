**Ne soruluyor?** İki ok aynı noktadan çizilse aralarında kaç derecelik açı olur?

**Fikir:** Nokta çarpımının geometrik anlamı açıyı verir:

$$
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

Bileşenlerden nokta çarpımını ve iki uzunluğu hesaplarsak, $\cos\theta$ tek bilinmeyen kalır. Kosinüsten de açıya geçeriz.

**Adım 1 — Nokta çarpımı.** Karşılıklı bileşenleri çarp, sonuçları topla:

$$
\begin{aligned}
\mathbf{a} \cdot \mathbf{b} &= 1 \cdot 1 + 1 \cdot 0 + 0 \cdot 1 \\
&= 1 + 0 + 0 = 1
\end{aligned}
$$

**Adım 2 — Uzunluklar.** Her vektör için bileşenlerin karelerini topla, karekökünü al:

$$
\begin{aligned}
\|\mathbf{a}\| &= \sqrt{1^2 + 1^2 + 0^2} = \sqrt{2} \\
\|\mathbf{b}\| &= \sqrt{1^2 + 0^2 + 1^2} = \sqrt{2}
\end{aligned}
$$

**Adım 3 — Kosinüs.** Formülü $\cos\theta$ için düzenle ve sayıları koy. $\sqrt{2} \cdot \sqrt{2} = 2$:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|} = \frac{1}{\sqrt{2} \cdot \sqrt{2}} = \frac{1}{2}
$$

**Adım 4 — Açı.** Kosinüsü $\tfrac{1}{2}$ olan açı $60°$ (bilinen açılardan: $\cos 0° = 1$, $\cos 60° = \tfrac{1}{2}$, $\cos 90° = 0$).

**Sonucu yorumla:** Kosinüs pozitif, yani açı $90°$'den küçük: iki vektör kabaca aynı tarafa bakıyor ama tam aynı yöne değil.

**Cevap:** $60°$.
