| Ölçü | Ne ölçer | Aralık | Not |
|---|---|---|---|
| Ortalama farkı | Merkezin kayması | Sınırsız | Şekil değişimini kaçırır |
| PSI | Kutulardaki payların ayrışması | 0 ve üstü | Başparmak kuralı: 0,1 / 0,25 |
| KS istatistiği | Birikimli dağılımlar arası en büyük uzaklık | 0 – 1 | Sayısal sütunlar |
| KS p-değeri | Farkın şansla çıkma olasılığı | 0 – 1 | Büyük örneklemde her şey "anlamlı" |
| Kategori payları | Her kategorinin payı | 0 – 1 | Kategorik sütunlarda PSI'nin kutuları |

## PSI adım adım

1. Referansı sırala, onda birlik dilimlerden 9 sınır al.
2. Her değeri `bisect_left(edges, v)` ile kutusuna koy.
3. Her kutunun payını hesapla, en az `0.0001`.
4. `Σ (güncel - referans) × ln(güncel / referans)`.

## Dersteki ölçüm (PSI)

| Ay | tenure | monthly_fee | support_calls | usage_hours |
|---|---|---|---|---|
| 0 (başka örneklem) | 0,012 | 0,013 | 0,004 | 0,016 |
| 2 | 0,005 | 0,229 | 0,055 | 0,121 |
| 3 | 0,012 | 0,456 | 0,109 | 0,284 |
| 6 | 0,012 | 1,875 | 0,280 | 1,152 |

3. ayda ücret "büyük kayma" gösterirken doğruluk 0,784'tü.

## Aynı kayma, üç örneklem (KS)

| Müşteri sayısı | İstatistik | p-değeri |
|---|---|---|
| 200 | 0,095 | 0,33 |
| 2000 | 0,083 | 2,1e-06 |
| 50 000 | 0,076 | 1,2e-124 |

## Terimler

- **Veri kayması** (data drift): girdilerin dağılımının zamanla değişmesi.
- **Referans** (reference): karşılaştırmanın temeli; çoğu zaman eğitim
  verisi.
- **Birikimli dağılım** (cumulative distribution): her `x` için
  değerlerin `x`'ten küçük ya da eşit olanlarının payı.
- **p-değeri** (p-value): farkın şansla bu kadar büyük çıkma olasılığı.
