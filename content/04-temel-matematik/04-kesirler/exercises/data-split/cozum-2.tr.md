**Fikir:** Önce testin tüm veriye oranını kesirlerle bul; örnek sayısını en sonda tek çarpmayla hesapla.

**Adım 1 — Eğitimden kalan.** $1 - \frac{7}{10} = \frac{3}{10}$.

**Adım 2 — Kalanın içinde test.** Doğrulama kalanın $\frac{1}{3}$'ü, test kalanın $1 - \frac{1}{3} = \frac{2}{3}$'ü.

**Adım 3 — Testin tüm veriye oranı.** Kesrin kesri, çarpım:

$$
\frac{2}{3} \cdot \frac{3}{10} = \frac{2}{10} = \frac{1}{5}
$$

**Adım 4 — Örnek sayısı.**

$$
\frac{1}{5} \cdot 1\,200 = 240
$$

**Neden aynı sonuç?** Birinci yol her adımda $1\,200$'lük bütünün sayılarıyla çalıştı; bu yol oranları çarpıp bütünle en sonda çarptı. Çarpma sırası değişse de aynı çarpımlar yapılıyor. Bu yolun artısı: veri setinin boyutu değişse bile testin payı $\frac{1}{5}$ olarak kalıyor.

**Cevap:** $240$ ve $\dfrac{1}{5}$.
