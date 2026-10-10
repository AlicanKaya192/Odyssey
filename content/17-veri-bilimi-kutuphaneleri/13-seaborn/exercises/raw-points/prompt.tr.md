`raw_points(hours, sales)` `sns.lineplot` ile çizsin ama aynı saatteki değerleri
**ortalamadan**, her kaydı ayrı nokta olarak (`estimator=None`). Şekli kapatıp
çizginin nokta sayısını döndürsün: `len(ax.lines[0].get_xdata())`. Başlangıç
kodu varsayılanı kullanıyor: aynı saatleri tek noktaya indiriyor.

**Beklenen çıktı:**

```
5
```
