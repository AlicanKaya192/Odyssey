**Ne soruluyor?** Para her yıl %8 büyüyor; 1000 liranın 2500 lira olması için gereken yıl sayısı. Bilinmeyen yıl sayısı **üste** duruyor, bu yüzden logaritma gerekecek.

**Fikir:** Her yıl %8 büyümek, her yıl $1.08$ ile çarpılmak demek. $t$ yıl sonra para $1000 \cdot 1.08^t$ olur. Üsteki $t$'yi indirmenin yolu iki tarafın logaritmasını almak; kuvvet kuralı ($\ln x^n = n \ln x$) üssü öne çeker.

**Adım 1 — Denklemi kur.**

$$
1000 \cdot 1.08^t = 2500
$$

**Adım 2 — Üslü terimi yalnız bırak.** İki tarafı 1000'e böl:

$$
1.08^t = 2.5
$$

Anlamı: para $2.5$ katına çıkmalı.

**Adım 3 — İki tarafın doğal logaritmasını al.** Eşit iki sayının logaritmaları da eşit. Kuvvet kuralı üssü öne indirir:

$$
\begin{aligned}
\ln (1.08^t) &= \ln 2.5 \\
t \cdot \ln 1.08 &= \ln 2.5
\end{aligned}
$$

**Adım 4 — $t$'yi yalnız bırak.** İki tarafı $\ln 1.08$'e böl ve verilen değerleri koy:

$$
\begin{aligned}
t &= \frac{\ln 2.5}{\ln 1.08} \\
&\approx \frac{0.9163}{0.0770} \\
&\approx 11.90
\end{aligned}
$$

Verilen yuvarlanmış değerlerle $11.90$, daha hassas değerlerle $11.91$ çıkıyor; ikisi de doğru kabul ediliyor.

**Sağlama (mantık kontrolü):** 11 yılda para $1.08^{11} \approx 2.33$ katına, 12 yılda $1.08^{12} \approx 2.52$ katına çıkıyor. $2.5$ kat ikisinin arasında ve 12'ye çok yakın. Sonuç makul. ✓

**Cevap:** yaklaşık 11.91 yıl.
