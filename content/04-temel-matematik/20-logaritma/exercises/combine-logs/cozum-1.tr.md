**Ne soruluyor?** Üç logaritmanın toplamı ve farkı tek bir sayıya eşit. Terimleri tek tek hesaplayamıyoruz (tam sayı değiller), o yüzden önce birleştirip sonra hesaplayacağız.

**Fikir:** Tabanları aynı logaritmalar birleştirilebilir:

$$
\begin{aligned}
\log_b x + \log_b y &= \log_b (x \cdot y) \quad (\text{çarpım kuralı}) \\
\log_b x - \log_b y &= \log_b \frac{x}{y} \quad (\text{bölüm kuralı})
\end{aligned}
$$

Neden? Logaritma bir üs. Üslü sayılar çarpılınca üsler toplanır ($b^m \cdot b^n = b^{m+n}$); logaritmada toplama bu yüzden içerideki çarpmaya karşılık geliyor.

**Adım 1 — Toplananları birleştir.** İki terimin tabanı da 6, çarpım kuralı uygulanabilir:

$$
\begin{aligned}
\log_6 12 + \log_6 18 &= \log_6 (12 \cdot 18) \\
&= \log_6 216
\end{aligned}
$$

**Adım 2 — Çıkarılanı birleştir.** Bölüm kuralıyla:

$$
\begin{aligned}
\log_6 216 - \log_6 6 &= \log_6 \frac{216}{6} \\
&= \log_6 36
\end{aligned}
$$

**Adım 3 — Değeri bul.** $\log_6 36$ şunu soruyor: 6'nın kaçıncı kuvveti 36? $6^2 = 36$, öyleyse:

$$
\log_6 36 = 2
$$

**Dikkat:** $\log_6 12 + \log_6 18$'i $\log_6 (12 + 18)$ diye birleştirmek yanlış. Logaritmada toplama içeride **çarpmaya** dönüşür.

**Cevap:** 2.
