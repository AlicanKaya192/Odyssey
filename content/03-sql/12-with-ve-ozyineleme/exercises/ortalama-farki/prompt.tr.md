İptal edilmeyen siparişlerde her müşterinin toplam harcamasını ve bunun
**müşteri ortalamasından farkını** göster.

Sütunlar: `name`, `total`, `vs_avg`. `total`'a göre büyükten küçüğe
sırala. Siparişi olmayan müşteri listede yok.

```
name           total     vs_avg
-------------  --------  ---------
Helix Studio   49690.00  29857.00
Bright Office  34100.00  14267.00
Delta Systems  6710.00   -13123.00
Orion Labs     4510.00   -15323.00
Nova Retail    4155.00   -15678.00
```

Ortalama beş müşterinin toplamlarının ortalaması (`19833.00`) — kalemlerin
ya da siparişlerin değil. Müşteri toplamlarını bir kez `WITH` ile
adlandırırsan aynı adı hem listede hem ortalamada kullanabilirsin.
