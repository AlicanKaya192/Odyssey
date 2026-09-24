**Ne soruluyor?** Bir olasılık yoğunluğunun toplam alanı, bir aralığın olasılığı ve medyan.

**Fikir:** Her olasılık yoğunluğun altındaki bir alan; ters türev $-e^{-2x}$.

**Adım 1 — Toplam.** $\int_0^{t} 2e^{-2x} \, dx = 1 - e^{-2t}$; $t \to \infty$ iken $e^{-2t} \to 0$: toplam $1$ ✓.

**Adım 2 — $P(X \le 1)$.** $1 - e^{-2} \approx 1 - 0{,}1353 = 0{,}8647$.

**Adım 3 — Medyan.** $1 - e^{-2m} = \frac{1}{2} \Rightarrow e^{-2m} = \frac{1}{2} \Rightarrow m = \frac{\ln 2}{2} \approx 0{,}347$.

**Sağlama:** Ortalama bekleme $E[X] = \frac{1}{2}$ dakika; medyan ($0{,}347$) ortalamadan küçük, çünkü dağılım sağa çarpık: kısa beklemeler çok, uzun beklemeler az ama uzun ✓.

**Dikkat:** $f(1) = 2e^{-2} \approx 0{,}27$ bir olasılık değil; yoğunluğun değeri. Olasılık alandır.

**Cevap:** $1$, $0{,}865$ ve $0{,}347$.
