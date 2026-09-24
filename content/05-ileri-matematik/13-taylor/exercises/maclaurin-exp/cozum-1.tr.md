**Ne soruluyor?** $e^x$'in üçüncü derece Taylor polinomunun bir katsayısı ve bir değeri.

**Fikir:** $P_3(x) = \sum_{k=0}^{3} \frac{f^{(k)}(0)}{k!} x^k$. $e^x$'in bütün türevleri $0$'da $1$.

**Adım 1 — Katsayılar.** $\frac{1}{0!}, \frac{1}{1!}, \frac{1}{2!}, \frac{1}{3!}$: $1, 1, \frac{1}{2}, \frac{1}{6}$. $x^3$'ün katsayısı $\frac{1}{6}$.

**Adım 2 — Değer.**

$$
\begin{aligned}
P_3(0{,}5) &= 1 + \frac{1}{2} + \frac{1}{8} + \frac{1}{48} \\
&= \frac{79}{48} \approx 1{,}6458
\end{aligned}
$$

**Sağlama:** $e^{0{,}5} \approx 1{,}6487$; fark $0{,}0029$. Atılan ilk terim $\frac{0{,}5^4}{24} \approx 0{,}0026$ ✓.

**Dikkat:** $\frac{x^3}{3}$ yazmak (faktöriyel yerine $3$) katsayıyı $\frac{1}{3}$ yapar; paydalar $1, 2, 6, 24$ diye büyür.

**Cevap:** $\frac{1}{6}$ ve $\frac{79}{48}$.
