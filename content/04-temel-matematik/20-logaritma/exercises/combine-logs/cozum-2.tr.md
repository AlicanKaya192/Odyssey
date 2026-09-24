**Fikir:** Bir terimi hemen sayıya çevirebiliyoruz: tabanın kendi logaritması her zaman 1, çünkü $6^1 = 6$. Bilinen değeri erkenden yerine koyarsak geriye daha küçük bir iş kalır.

**Adım 1 — Bilinen terimi sayıya çevir.** $\log_6 6 = 1$:

$$
\log_6 12 + \log_6 18 - \log_6 6 = \log_6 12 + \log_6 18 - 1
$$

**Adım 2 — Kalan iki terimi birleştir.** Çarpım kuralıyla ($\log_b x + \log_b y = \log_b xy$):

$$
\log_6 12 + \log_6 18 = \log_6 (12 \cdot 18) = \log_6 216
$$

**Adım 3 — $216$'yı 6'nın kuvveti olarak yaz.** $216 = 6 \cdot 36 = 6 \cdot 6 \cdot 6 = 6^3$. Öyleyse:

$$
\log_6 216 = \log_6 6^3 = 3
$$

**Adım 4 — Çıkarmayı yap.**

$$
3 - 1 = 2
$$

**Neden aynı sonuç?** Birinci yol her şeyi tek bir logaritmaya indirip en sonda hesapladı ($\log_6 36$). Bu yol bilinen bir değeri baştan sayıya çevirdi. İkisi de aynı kuralları kullanıyor, yalnızca sıra farklı.

**Cevap:** 2.
