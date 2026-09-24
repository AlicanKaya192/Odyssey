**Ne soruluyor?** İç içe fonksiyon içeren iki belirli integral.

**Fikir:** İçte bir fonksiyon ve türevi birlikte duruyorsa $u$ o fonksiyon. Belirli integralde sınırlar da $u$'ya çevrilir.

**Adım 1 — Birinci.** $u = x^2 + 1$, $du = 2x \, dx$; $x = 0 \to u = 1$, $x = 1 \to u = 2$:

$$
\int_1^2 u^3 \, du = \left[\frac{u^4}{4}\right]_1^2 = \frac{16 - 1}{4} = \frac{15}{4}
$$

**Adım 2 — İkinci.** $u = 2x$, $du = 2 \, dx$; sınırlar $0$ ve $2 \ln 2$:

$$
\frac{1}{2} \int_0^{2 \ln 2} e^u \, du = \frac{1}{2}\left(e^{2 \ln 2} - 1\right) = \frac{1}{2}(4 - 1) = \frac{3}{2}
$$

**Sağlama:** $e^{2 \ln 2} = (e^{\ln 2})^2 = 2^2 = 4$ ✓.

**Dikkat:** $u$'ya geçip sınırları $0$ ve $1$ bırakmak birincide $\frac{1}{4}$ verir; sınırlar değişkenle birlikte değişir.

**Cevap:** $\frac{15}{4}$ ve $\frac{3}{2}$.
