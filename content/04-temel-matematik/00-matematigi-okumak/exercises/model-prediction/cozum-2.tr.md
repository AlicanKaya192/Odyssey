**Fikir:** Özellikleri, ağırlıkları ve çarpımları bir tabloya yazınca hangi özelliğin tahmini ne yöne ittiği bir bakışta görünüyor. Modelleri açıklarken tam olarak böyle tablolar kullanılıyor.

**Adım 1 — Tabloyu kur.**

| Parça | Değer | Ağırlık | Katkı |
|---|---|---|---|
| $x_1$ | $80$ | $0.5$ | $+40$ |
| $x_2$ | $6$ | $-2$ | $-12$ |
| sabit $b$ | | | $+10$ |

**Adım 2 — Katkıları topla.**

$$
40 - 12 + 10 = 38
$$

**Adım 3 — Kare hata.** $(35 - 38)^2 = (-3)^2 = 9$. Farkı ters sırayla alsan da ($\hat{y} - y = 3$) karesi aynı: $3^2 = 9$.

**Sonucu yorumla:** Tablo, $x_2$'nin negatif ağırlığı yüzünden tahmini $12$ birim **aşağı** çektiğini gösteriyor. Ağırlığın işareti, o özelliğin tahmini artırıp artırmadığını söylüyor.

**Cevap:** $38$ ve $9$.
