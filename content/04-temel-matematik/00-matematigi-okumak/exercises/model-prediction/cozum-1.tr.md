**Ne soruluyor?** Bir makine öğrenmesi formülünü okuyup sayıları yerine koymak: önce tahmin, sonra tahminin ne kadar yanlış olduğu.

**Fikir:** $w_1 x_1$ "birinci ağırlık çarpı birinci özellik". Her özellik kendi ağırlığıyla çarpılıyor, sonuçlar toplanıyor, sabit ekleniyor. Kare hata, gerçek değerle tahmin arasındaki farkın karesi.

**Adım 1 — Her özelliğin katkısı.**

$$
\begin{aligned}
w_1 x_1 &= 0.5 \cdot 80 = 40 \\
w_2 x_2 &= -2 \cdot 6 = -12
\end{aligned}
$$

**Adım 2 — Topla ve sabiti ekle.**

$$
\hat{y} = 40 + (-12) + 10 = 38
$$

**Adım 3 — Hata.** Gerçek değer ile tahmin arasındaki fark:

$$
y - \hat{y} = 35 - 38 = -3
$$

Model 3 birim fazla tahmin etmiş.

**Adım 4 — Karesi.**

$$
(-3)^2 = 9
$$

**Sonucu yorumla:** Kare almak iki işe yarıyor: hatanın yönünü (fazla mı eksik mi) siliyor, çünkü $(-3)^2 = 3^2$; ve büyük hataları küçüklerden çok daha fazla cezalandırıyor ($10$'luk hata $100$ puan, $1$'lik hata $1$ puan). Modeller eğitilirken bu kare hataların ortalaması küçültülüyor.

**Cevap:** $\hat{y} = 38$, kare hata $9$.
