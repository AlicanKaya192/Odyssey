**Ne soruluyor?** Bir polinom modelinin iki noktadaki tahmini ve bir örnekteki hatası.

**Fikir:** Tahmin, polinomun o noktadaki değeri. Hata, gerçek değer eksi tahmin.

**Adım 1 — $x = 2$.** $x^2 = 4$, $x^3 = 8$.

$$
\begin{aligned}
\hat{y} &= 1 + 2 \cdot 2 - 1 \cdot 4 + 0{,}5 \cdot 8 \\
&= 1 + 4 - 4 + 4 = 5
\end{aligned}
$$

**Adım 2 — $x = -2$.** $x^2 = 4$, $x^3 = -8$.

$$
\begin{aligned}
\hat{y} &= 1 + 2 \cdot (-2) - 4 + 0{,}5 \cdot (-8) \\
&= 1 - 4 - 4 - 4 = -11
\end{aligned}
$$

**Adım 3 — Hata.** $y - \hat{y} = 6 - 5 = 1$. Model bu örnekte $1$ birim az tahmin etmiş.

**Sağlama:** Çift kuvvetli terimler ($1$ ve $-x^2$) iki noktada aynı: $1 - 4 = -3$. Tek kuvvetliler ($2x + 0{,}5x^3$) yalnızca işaret değiştirir: $+8$ ve $-8$. $-3 + 8 = 5$, $-3 - 8 = -11$ ✓.

**Dikkat:** $w_2 = -1$ ile $x^2 = 4$'ün çarpımı $-4$; kareyi negatif sayıya uygulamak ($(-2)^2$) ile katsayının eksisini karıştırma.

**Cevap:** $\hat{y}(2) = 5$, $\hat{y}(-2) = -11$, hata $1$.
