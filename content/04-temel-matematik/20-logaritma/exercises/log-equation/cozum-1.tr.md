**Ne soruluyor?** Denklemi sağlayan $x$ değeri. Soru bir tuzağı da haber veriyor: cebir birden fazla aday verebilir, ama hepsi geçerli olmayabilir.

**Fikir:** Üç adımda ilerleyeceğiz:

1. İki logaritmayı çarpım kuralıyla tek logaritmaya indir.
2. Logaritmanın tanımıyla ($\log_2 A = 4$ demek $A = 2^4$ demek) logaritmadan kurtul; geriye ikinci dereceden bir denklem kalır.
3. Bulunan her adayı **orijinal** denklemde dene, çünkü logaritmanın içi pozitif olmak zorunda.

**Adım 1 — Çarpım kuralıyla birleştir.** $\log_b x + \log_b y = \log_b (xy)$:

$$
\log_2 \big((x + 2)(x - 4)\big) = 4
$$

**Adım 2 — Tanıma çevir.** "$2$'nin 4. kuvveti içerideki ifadeye eşit":

$$
(x + 2)(x - 4) = 2^4 = 16
$$

**Adım 3 — Parantezi aç ve sıfıra eşitle.**

$$
\begin{aligned}
x^2 - 4x + 2x - 8 &= 16 \\
x^2 - 2x - 8 - 16 &= 0 \\
x^2 - 2x - 24 &= 0
\end{aligned}
$$

**Adım 4 — Çarpanlarına ayır.** Çarpımı $-24$, toplamı $-2$ olan iki sayı arıyoruz: $-6$ ve $4$ ($-6 \cdot 4 = -24$, $-6 + 4 = -2$).

$$
(x - 6)(x + 4) = 0
$$

Bir çarpım ancak çarpanlardan biri sıfırsa sıfır olur, o yüzden iki aday var: $x = 6$ ya da $x = -4$.

**Adım 5 — Her adayı orijinal denklemde dene.** Logaritmanın içi pozitif olmalı:

| Aday | $x + 2$ | $x - 4$ | Geçerli mi? |
|---|---|---|---|
| $x = 6$ | $8 > 0$ | $2 > 0$ | ✓ |
| $x = -4$ | $-2 < 0$ | $-8 < 0$ | ✕ (negatifin logaritması yok) |

**Sağlama:** $x = 6$ için

$$
\log_2 8 + \log_2 2 = 3 + 1 = 4
$$

Tutuyor. ✓

**Sahte çözüm nereden geldi?** Adım 1'de iki logaritmayı birleştirdik. $x = -4$ için $(x + 2)(x - 4) = (-2)(-8) = 16$ pozitif, birleşik hâl tanımlı görünüyor. Ama orijinal denklemdeki $\log_2(-2)$ ve $\log_2(-8)$ tanımsız. Birleştirmek bu şartı gizledi, kontrol onu geri getirdi.

**Cevap:** 6.
