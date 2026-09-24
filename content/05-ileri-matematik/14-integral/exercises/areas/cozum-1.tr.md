**Ne soruluyor?** İki eğri arasındaki ve bir eğri ile eksen arasındaki alan.

**Fikir:** İki eğri arasındaki alan $\int (\text{üstteki} - \text{alttaki}) \, dx$. Eksenle arasındaki alan için önce eğrinin ekseni kestiği yerleri bul.

**Adım 1 — Birinci alan.** $[0, 1]$'de $x \ge x^2$:

$$
\int_0^1 (x - x^2) \, dx = \left[\frac{x^2}{2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}
$$

**Adım 2 — Sınırlar.** $4 - x^2 = 0 \Rightarrow x = -2$, $x = 2$. Aradaki $f \ge 0$.

**Adım 3 — İkinci alan.**

$$
\left[4x - \frac{x^3}{3}\right]_{-2}^{2} = \left(8 - \frac{8}{3}\right) - \left(-8 + \frac{8}{3}\right) = \frac{32}{3}
$$

**Sağlama:** İkinci alan, tabanı $4$, yüksekliği $4$ olan dikdörtgenin ($16$) üçte ikisi: parabol parçasının alanı hep böyledir (Arşimet) ✓.

**Dikkat:** Birincide $\int (x^2 - x)$ yazmak $-\frac{1}{6}$ verir; alan pozitif olmalı, üstteki eğriden alttakini çıkar.

**Cevap:** $\frac{1}{6}$ ve $\frac{32}{3}$.
