**Fikir:** Açılımı ezberden değil, Taylor formülünden kur: $f(x) = \ln(1 + x)$'in $0$'daki türevlerini hesapla.

**Adım 1 — Türevler.** $f' = (1 + x)^{-1}$, $f'' = -(1 + x)^{-2}$, $f''' = 2(1 + x)^{-3}$. $0$'da: $f(0) = 0$, $f'(0) = 1$, $f''(0) = -1$, $f'''(0) = 2$.

**Adım 2 — Katsayılar.** $\frac{1}{1!} = 1$, $\frac{-1}{2!} = -\frac{1}{2}$, $\frac{2}{3!} = \frac{1}{3}$: $x - \frac{x^2}{2} + \frac{x^3}{3}$.

**Adım 3 — Değerler.** İki terim $0{,}18$; üçüncü terim $\frac{0{,}008}{3}$.

**Neden aynı sonuç?** Tablodaki açılım bu türevlerden geliyor; $k$'ıncı türev $(-1)^{k-1}(k - 1)!$ olduğu için $k!$'e bölünce $\frac{(-1)^{k-1}}{k}$ kalıyor: paydalar $1, 2, 3, \ldots$, işaretler sırayla.

**Cevap:** $0{,}18$ ve $\approx 0{,}0027$.
