**Fikir:** $100$ e-postayı iki soruya göre dört kutuya ayır: model ne dedi, gerçek ne? Bu tabloya **karışıklık matrisi** denir; ölçülerin hepsi buradan okunur.

**Adım 1 — Kutular.**

| | gerçek spam | gerçek normal | toplam |
|---|---|---|---|
| model: spam | $24$ | $30 - 24 = 6$ | $30$ |
| model: normal | $40 - 24 = 16$ | $54$ | $70$ |
| toplam | $40$ | $60$ | $100$ |

**Adım 2 — Kesinlik.** "Model: spam" satırı: $\dfrac{24}{30} = 0{,}8$.

**Adım 3 — Duyarlılık.** "Gerçek spam" sütunu: $\dfrac{24}{40} = 0{,}6$.

**Neden aynı sonuç?** Tablonun dört kutusu, iki kümenin Venn şemasındaki dört bölgesi: $T \cap G$ ($24$), yalnız $T$ ($6$), yalnız $G$ ($16$), hiçbiri ($54$). Kesinlik satıra, duyarlılık sütuna bakıyor.

**Cevap:** $0{,}8$ ve $0{,}6$.
