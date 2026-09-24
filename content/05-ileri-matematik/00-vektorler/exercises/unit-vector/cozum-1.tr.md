**Ne soruluyor?** Birim vektör, uzunluğu tam 1 olan vektör. $\mathbf{v}$ ile aynı yönü gösteren ama boyu 1 olan oku arıyoruz.

**Fikir:** Bir vektörü pozitif bir sayıya bölmek yönünü değiştirmez, yalnızca boyunu küçültür. Boyu 10 olan bir oku 10'a bölersek boyu 1 olur. Yani önce uzunluğu bul, sonra her bileşeni o uzunluğa böl.

**Adım 1 — Uzunluğu bul.**

$$
\begin{aligned}
\|\mathbf{v}\| &= \sqrt{6^2 + (-8)^2} \\
&= \sqrt{36 + 64} \\
&= \sqrt{100} = 10
\end{aligned}
$$

**Adım 2 — Her bileşeni uzunluğa böl.**

$$
\begin{aligned}
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|} &= \left(\frac{6}{10},\ \frac{-8}{10}\right) \\
&= (0.6,\ -0.8)
\end{aligned}
$$

**Sağlama:** Boyu gerçekten 1 mi?

$$
\sqrt{0.6^2 + (-0.8)^2} = \sqrt{0.36 + 0.64} = \sqrt{1} = 1
$$

Yön de aynı kaldı: iki bileşen aynı sayıya bölündüğü için aralarındaki oran değişmedi ve işaretler yerinde durdu. ✓

**Dikkat:** Eksi işareti atılmaz. $(0.6,\ 0.8)$ de birim vektör, ama başka bir yönü gösteriyor.

**Ne işe yarar?** Birim vektör yalnızca yönü taşıyor. İki vektörün yönlerini boylarından bağımsız karşılaştırmak için (bir sonraki bölümdeki kosinüs benzerliği gibi) önce ikisi de birim yapılır.

**Cevap:** $(0.6, -0.8)$.
