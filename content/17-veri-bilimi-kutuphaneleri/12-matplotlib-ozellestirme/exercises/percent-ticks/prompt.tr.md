`percent_ticks(rates)` 0–1 arasında saklanan oranları çizgi grafiğe çizsin ve y
ekseni yazılarını **ondalıksız yüzde** olarak yazsın
(`PercentFormatter(xmax=1, decimals=0)`). Şekli çizdirip y ekseninin ilk
**üç** işaret yazısını döndürsün ve şekli kapatsın. Başlangıç kodu
`xmax=100` kullanıyor: 0,184'ü `%0,184` gibi yazıyor.

**Beklenen çıktı:**

```
['0%', '5%', '10%']
```
