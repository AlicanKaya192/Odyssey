**Ne soruluyor?** $\mathbf{b}$'nin doğrultusuna dik bir ışık tutulduğunu düşün: $\mathbf{a}$'nın o doğru üzerine düşen gölgesi. Birinci soru gölgenin uzunluğu (tek bir sayı), ikinci soru gölgenin kendisi (bir vektör).

**Fikir:** Nokta çarpımı $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\cos\theta \cdot \|\mathbf{b}\|$. Buradaki $\|\mathbf{a}\|\cos\theta$ tam olarak gölgenin uzunluğu. Yani nokta çarpımını $\|\mathbf{b}\|$'ye bölersek gölge uzunluğu kalır. Gölge vektörü de $\mathbf{b}$ yönünde, bu uzunlukta bir ok.

**Adım 1 — Gerekli parçalar.**

$$
\begin{aligned}
\mathbf{a} \cdot \mathbf{b} &= 6 \cdot 3 + 2 \cdot 4 = 18 + 8 = 26 \\
\mathbf{b} \cdot \mathbf{b} &= 3^2 + 4^2 = 9 + 16 = 25 \\
\|\mathbf{b}\| &= \sqrt{25} = 5
\end{aligned}
$$

**Adım 2 — Skaler izdüşüm (gölgenin uzunluğu).**

$$
\frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|} = \frac{26}{5} = 5.2
$$

**Adım 3 — Vektör izdüşüm (gölgenin kendisi).** $\mathbf{b}$'yi öyle bir sayıyla çarpıyoruz ki uzunluğu $5.2$ olsun. Bu sayı $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}$: bir kez $\|\mathbf{b}\|$'ye bölüp uzunluğu buluyor, bir kez daha bölüp $\mathbf{b}$'yi birim boya indiriyor.

$$
\begin{aligned}
\frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b} &= \frac{26}{25}\,(3,\ 4) \\
&= (1.04 \cdot 3,\ 1.04 \cdot 4) \\
&= (3.12,\ 4.16)
\end{aligned}
$$

**Sağlama:** Gölge doğruysa, $\mathbf{a}$'dan gölgeyi çıkarınca kalan parça $\mathbf{b}$'ye dik olmalı:

$$
\begin{aligned}
\mathbf{a} - (3.12,\ 4.16) &= (2.88,\ -2.16) \\
(2.88,\ -2.16) \cdot (3,\ 4) &= 8.64 - 8.64 = 0
\end{aligned}
$$

Dik. ✓ Ayrıca gölgenin uzunluğu $\sqrt{3.12^2 + 4.16^2} = 5.2$, birinci cevapla aynı.

**Dikkat:** Vektör izdüşümde payda $\mathbf{b} \cdot \mathbf{b} = 25$, $\|\mathbf{b}\| = 5$ değil. $5$'e bölersen gölge 5 kat uzun çıkar.

**Cevap:** $5.2$ ve $(3.12,\ 4.16)$.
