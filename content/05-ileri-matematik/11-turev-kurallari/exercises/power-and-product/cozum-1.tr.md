**Ne soruluyor?** Kuvvetlerden oluşan bir fonksiyonun ve bir çarpımın türevinin bir noktadaki değeri.

**Fikir:** Kökü ve kesri üs olarak yazınca her terim kuvvet kuralına girer. Çarpımda çarpım kuralı.

**Adım 1 — $f'$.** $f(x) = x^3 - 4x^{1/2} + 2x^{-1}$:

$$
f'(x) = 3x^2 - 2x^{-1/2} - 2x^{-2} = 3x^2 - \frac{2}{\sqrt{x}} - \frac{2}{x^2}
$$

**Adım 2 — $f'(4)$.** $48 - \frac{2}{2} - \frac{2}{16} = 48 - 1 - 0{,}125 = 46{,}875 = \frac{375}{8}$.

**Adım 3 — $h'$.** $h'(x) = 2x(x - 3) + (x^2 + 1)$; $h'(2) = 4 \cdot (-1) + 5 = 1$.

**Sağlama:** $h$ için merkezi fark, $h = 0{,}01$: $h(2{,}01) = 5{,}0401 \cdot (-0{,}99) = -4{,}989699$, $h(1{,}99) = 4{,}9601 \cdot (-1{,}01) = -5{,}009701$; fark bölü $0{,}02$: $1{,}0001$ ✓.

**Dikkat:** $-4\sqrt{x}$'in türevinde katsayı $-4 \cdot \frac{1}{2} = -2$; $\frac{2}{x}$'in türevinde işaret eksi olur.

**Cevap:** $f'(4) = \frac{375}{8} = 46{,}875$, $h'(2) = 1$.
