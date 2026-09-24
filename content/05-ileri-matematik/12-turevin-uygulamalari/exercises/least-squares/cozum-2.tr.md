**Fikir:** Kayıp $w$'nin ikinci dereceden bir fonksiyonu; açıp tepe noktasını $-\frac{b}{2a}$ ile bul.

**Adım 1 — Aç.**

$$
\begin{aligned}
L(w) &= (2 - w)^2 + (3 - 2w)^2 + (7 - 3w)^2 \\
&= 14w^2 - 58w + 62
\end{aligned}
$$

**Adım 2 — Tepe.** $w = \frac{58}{2 \cdot 14} = \frac{29}{14}$. En küçük değer $62 - \frac{58^2}{4 \cdot 14} = 62 - \frac{3364}{56} = \frac{27}{14}$.

**Adım 3 — Sabit model.** $L(c) = 3c^2 - 24c + 62$, tepe $c = \frac{24}{6} = 4$.

**Neden aynı sonuç?** $14w^2 - 58w + 62$'de $14 = \sum x_i^2$, $58 = 2 \sum x_i y_i$, $62 = \sum y_i^2$. Tepe formülü $\frac{58}{28}$ tam olarak $\frac{\sum x_i y_i}{\sum x_i^2}$; türevi sıfırlamak ile tepe noktası aynı hesap.

**Cevap:** $\frac{29}{14}$, $\frac{27}{14}$ ve $4$.
