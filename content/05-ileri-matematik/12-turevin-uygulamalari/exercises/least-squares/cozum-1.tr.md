**Ne soruluyor?** Üç noktalı bir veride iki basit modelin en iyi parametresi ve en küçük kayıp.

**Fikir:** Kaybı parametrenin fonksiyonu olarak yaz, türevini sıfıra eşitle.

**Adım 1 — Türev.** $L(w) = \sum (y_i - w x_i)^2$, $L'(w) = -2 \sum x_i (y_i - w x_i) = 0$:

$$
w = \frac{\sum x_i y_i}{\sum x_i^2} = \frac{2 + 6 + 21}{1 + 4 + 9} = \frac{29}{14} \approx 2{,}071
$$

**Adım 2 — Kayıp.** Artıklar: $2 - \frac{29}{14} = -\frac{1}{14}$, $3 - \frac{58}{14} = -\frac{16}{14}$, $7 - \frac{87}{14} = \frac{11}{14}$. Kareler toplamı $\frac{1 + 256 + 121}{196} = \frac{378}{196} = \frac{27}{14} \approx 1{,}93$.

**Adım 3 — Sabit model.** $L(c) = \sum (y_i - c)^2$, $L'(c) = 0 \Rightarrow c = \frac{2 + 3 + 7}{3} = 4$.

**Sağlama:** $L''(w) = 2 \sum x_i^2 = 28 > 0$: gerçekten en küçük ✓. $w = 2$ ile kayıp $0 + 1 + 1 = 2 > \frac{27}{14}$ ✓.

**Dikkat:** $w$'yi $\frac{\sum y_i}{\sum x_i} = \frac{12}{6} = 2$ diye bulmak yanlış; o, karesel hatayı en küçük yapan değer değil.

**Cevap:** $w = \frac{29}{14}$, kayıp $\frac{27}{14}$, $c = 4$.
