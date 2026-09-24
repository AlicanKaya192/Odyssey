**Ne soruluyor?** Bir aralıktaki ortalama hız ve bir andaki hız.

**Fikir:** Ortalama hız kesenin eğimi; anlık hız aralık sıfıra giderken bu eğimin limiti, yani türev.

**Adım 1 — Ortalama.** $s(1) = 5$, $s(3) = 45$: $\frac{45 - 5}{3 - 1} = 20$.

**Adım 2 — Anlık.**

$$
\begin{aligned}
\frac{s(3 + h) - s(3)}{h} &= \frac{5(9 + 6h + h^2) - 45}{h} \\
&= 30 + 5h \;\to\; 30
\end{aligned}
$$

**Sağlama:** $s'(t) = 10t$ (tanımdan $5 \cdot 2t$), $s'(3) = 30$ ✓. İlginç bir ayrıntı: ortalama hız $20$, aralığın ortası $t = 2$'deki anlık hıza, $s'(2) = 20$'ye eşit; parabollerde hep böyle.

**Dikkat:** Ortalama hızı iki uçtaki hızların ortalaması sanmak ($\frac{10 + 30}{2} = 20$) burada tesadüfen tutuyor; genel yöntem yol bölü süre.

**Cevap:** $20$ m/s ve $30$ m/s.
