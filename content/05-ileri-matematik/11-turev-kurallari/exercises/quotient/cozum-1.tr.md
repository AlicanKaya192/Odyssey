**Ne soruluyor?** Bir kesirli fonksiyonun türevinin bir noktadaki değeri ve türevin sıfır olduğu yer.

**Fikir:** $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$. Türev sıfırsa pay sıfır.

**Adım 1 — Türev.**

$$
f'(x) = \frac{1 \cdot (x^2 + 1) - x \cdot 2x}{(x^2 + 1)^2} = \frac{1 - x^2}{(x^2 + 1)^2}
$$

**Adım 2 — $f'(2)$.** $\frac{1 - 4}{25} = -\frac{3}{25} = -0{,}12$.

**Adım 3 — Sıfır.** $1 - x^2 = 0 \Rightarrow x = \pm 1$; pozitif olan $x = 1$.

**Sağlama:** $x = 1$'de $f(1) = \frac{1}{2}$; $f(0{,}9) = \frac{0{,}9}{1{,}81} \approx 0{,}497$, $f(1{,}1) = \frac{1{,}1}{2{,}21} \approx 0{,}498$. İki yan da $0{,}5$'ten küçük: $x = 1$ bir tepe, türevin sıfır olması beklendiği gibi ✓.

**Dikkat:** Paydaki sırayı çevirmek ($x \cdot 2x - (x^2 + 1)$) $f'(2) = +\frac{3}{25}$ verir; $x = 2$'de fonksiyon azalıyor, türev negatif olmalı.

**Cevap:** $f'(2) = -\frac{3}{25}$, $x = 1$.
