**Ne soruluyor?** Bir sınıflandırıcının iki temel başarı ölçüsü.

**Fikir:** İki ölçü de doğru yakalananları ($T \cap G$) bir bütüne bölüyor; fark, bütünün ne olduğunda. Kesinlikte bütün "modelin spam dedikleri", duyarlılıkta "gerçek spamler".

**Adım 1 — Kesişim.** Modelin spam dediği ve gerçekten spam olan: $s(T \cap G) = 24$.

**Adım 2 — Kesinlik.**

$$
\frac{24}{30} = 0{,}8
$$

Modelin spam dediklerinin $\%80$'i gerçekten spam.

**Adım 3 — Duyarlılık.**

$$
\frac{24}{40} = 0{,}6
$$

Gerçek spamlerin $\%60$'ı yakalanmış; $16$ spam kaçmış.

**Sonucu yorumla:** Model temkinli: "spam" dediğinde çoğunlukla haklı (yüksek kesinlik) ama birçok spami kaçırıyor (düşük duyarlılık). Eşiği düşürmek duyarlılığı artırır, genelde kesinliği düşürür.

**Dikkat:** İki paydayı karıştırmak en sık hata. Kesinlik "benim dediklerim içinde", duyarlılık "gerçekte olanlar içinde".

**Cevap:** Kesinlik $0{,}8$, duyarlılık $0{,}6$.
