**Fikir:** Bir kez $F(t) = P(X \le t)$'yi (**birikimli dağılım fonksiyonu**) kur; bütün sorular ondan okunur.

**Adım 1 — $F$.** $F(t) = \int_0^t 2e^{-2x} \, dx = \big[-e^{-2x}\big]_0^t = 1 - e^{-2t}$.

**Adım 2 — Oku.** Toplam: $\lim_{t \to \infty} F(t) = 1$. $P(X \le 1) = F(1) = 0{,}8647$.

**Adım 3 — Tersini al.** $F(m) = \frac{1}{2}$: $m = \frac{\ln 2}{2}$.

**Neden aynı sonuç?** Temel teorem: $F$, yoğunluğun ters türevi ve $F' = f$. Her olasılık $F$'nin iki değerinin farkı: $P(a \le X \le b) = F(b) - F(a)$. İstatistik kütüphanelerindeki `cdf` fonksiyonları tam olarak bu $F$.

**Cevap:** $1$, $0{,}865$, $0{,}347$.
