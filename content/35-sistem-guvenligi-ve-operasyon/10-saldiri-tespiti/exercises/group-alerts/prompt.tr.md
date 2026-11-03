Her uyarı `[saniye, kaynak]`. `group_alerts(alerts, gap)` uyarıları
kaynağa göre gruplasın: aynı kaynağın zamana göre sıralı uyarılarında iki
uyarı arası `gap` saniyeden **uzun değilse** aynı olaydır. Her olay için
`"<kaynak> <ilk>-<son> (<adet>)"` satırını döndürsün; kaynağa, sonra ilk
saniyeye göre sıralı.

**Beklenen çıktı:**

```
198.51.100.4 30-30 (1)
203.0.113.9 10-15 (3)
203.0.113.9 90-90 (1)
```
