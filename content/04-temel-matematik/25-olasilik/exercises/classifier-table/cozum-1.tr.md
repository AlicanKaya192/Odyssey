**Ne soruluyor?** Bir sınıflandırıcının tahmin olasılığı, doğruluğu ve "kedi" dediğinde haklı çıkma olasılığı.

**Fikir:** Sayıları iki yönlü tabloya koy; her olasılık bir hücre bölü doğru toplam.

**Adım 1 — Tablo.**

| gerçek \ tahmin | kedi | köpek | toplam |
|---|---|---|---|
| kedi | $70$ | $10$ | $80$ |
| köpek | $20$ | $100$ | $120$ |
| toplam | $90$ | $110$ | $200$ |

**Adım 2 — "Kedi" deme ve doğruluk.** $\frac{90}{200} = 0{,}45$. Doğrular köşegende: $\frac{70 + 100}{200} = 0{,}85$.

**Adım 3 — "Kedi" dediyse.** Payda "kedi" sütunu: $\frac{70}{90} = \frac{7}{9} \approx 0{,}78$.

**Sağlama:** $P(\text{kedi der} \mid \text{gerçek kedi}) = \frac{70}{80} = 0{,}875$; bu, üçüncü sorunun cevabından farklı ✓, çünkü paydalar farklı gruplar.

**Dikkat:** Üçüncü soru makine öğrenmesinde **kesinlik** (precision) diye anılır; $\frac{70}{80}$ ise **duyarlılık** (recall). İkisini karıştırmak sık yapılan hata.

**Cevap:** $0{,}45$, $0{,}85$, $\frac{7}{9}$.
