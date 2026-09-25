**Fikir:** $\sum (x - \bar{x})(y - \bar{y}) = \sum xy - n\bar{x}\bar{y}$.

**Adım 1 — Kovaryans.** $\sum xy = 100 + 180 + 325 + 450 + 810 = 1865$. $n\bar{x}\bar{y} = 5 \cdot 5 \cdot 68 = 1700$. Fark $165$; $\frac{165}{4} = 41{,}25$.

**Adım 2 — Korelasyon.** $\sum x^2 - n\bar{x}^2 = 155 - 125 = 30$ ve $\sum y^2 - n\bar{y}^2 = 24050 - 23120 = 930$.

$$
r = \frac{165}{\sqrt{30 \cdot 930}} = \frac{165}{167{,}03} \approx 0{,}988
$$

**Adım 3 — Dakika.** $\sum xy$ ve $n\bar{x}\bar{y}$ ikisi de $60$ ile çarpılır: $2475$.

**Neden aynı sonuç?** $E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - \mu_X\mu_Y$ özdeşliğinin toplam hâli; $r$'de $n - 1$ pay ve paydada sadeleştiği için doğrudan toplamlarla çalışılabiliyor.

**Cevap:** $41{,}25$; $0{,}988$ ve $2475$.
