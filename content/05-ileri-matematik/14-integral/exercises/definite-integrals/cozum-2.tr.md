**Fikir:** Birinci integrali terimlere ayır ve doğrusal terimi geometriyle (yamuk alanı) bul. İkincide $x = t^2$ ile kökten kurtul.

**Adım 1 — Terimler.** $\int_1^3 3x^2 \, dx = \big[x^3\big]_1^3 = 26$. $\int_1^3 x \, dx$: $y = x$ doğrusunun altında, $x = 1$'den $3$'e bir yamuk; paralel kenarlar $1$ ve $3$, yükseklik $2$: alan $\frac{(1 + 3) \cdot 2}{2} = 4$. Toplam $26 - 2 \cdot 4 = 18$.

**Adım 2 — Değişken değiştir.** $x = t^2$, $dx = 2t \, dt$; $x = 1 \to t = 1$, $x = 4 \to t = 2$:

$$
\int_1^4 \frac{dx}{\sqrt{x}} = \int_1^2 \frac{2t}{t} \, dt = \int_1^2 2 \, dt = 2
$$

**Neden aynı sonuç?** Doğrusal bir fonksiyonun integrali gerçekten bir yamuğun alanı; temel teorem aynı sayıyı formülle veriyor. İkincide değişken değiştirme, kökü sabit bir fonksiyona çevirdi: yüksekliği $2$, genişliği $1$ olan bir dikdörtgen.

**Cevap:** $18$ ve $2$.
