**Ne soruluyor?** Kesilen kare kenarının, kutunun hacmini en büyük yapan değeri.

**Fikir:** Hacmi $x$ cinsinden yaz, türevini sıfıra eşitle. Türevde ortak çarpan ayrılınca kökler hemen görünüyor.

**Adım 1 — Hacim.** $V(x) = x(12 - 2x)^2$, $0 < x < 6$.

**Adım 2 — Türev.** Çarpım kuralı, ikinci çarpanda zincir: $\big((12 - 2x)^2\big)' = 2(12 - 2x) \cdot (-2)$.

$$
\begin{aligned}
V'(x) &= (12 - 2x)^2 - 4x(12 - 2x) \\
&= (12 - 2x)(12 - 6x)
\end{aligned}
$$

**Adım 3 — Kökler.** $x = 6$ (hacim sıfır, kutu yok) ya da $x = 2$.

**Adım 4 — Hacim.** $V(2) = 2 \cdot 8^2 = 128$.

**Sağlama:** $V(1) = 1 \cdot 100 = 100$, $V(3) = 3 \cdot 36 = 108$. İkisi de $128$'den küçük ✓.

**Dikkat:** Zincir kuralındaki $-2$'yi unutmak $V' = (12 - 2x)(12 - 2x + 2x)$ gibi yanlış bir ifade verir ve kritik nokta kaybolur.

**Cevap:** $x = 2$ cm, $V = 128$ cm³.
