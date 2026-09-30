2023 ve 2024'ü birikimli olarak karşılaştır: hangisi 50 bin birime daha
erken ulaştı?

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `s` serisi olarak oku.
2. Her iki yıl için birikimli toplamı hesapla:
   `s.loc["2023"].cumsum()` ve `s.loc["2024"].cumsum()`.
3. Her yılın 50000'e ilk ulaştığı tarihi (`"%Y-%m-%d"`) alt alta yazdır.
   İpucu: `(ytd >= 50000).idxmax()` koşulun ilk doğru olduğu tarihi verir.
4. 30 Haziran'daki birikimli toplamları (önce 2023, sonra 2024) aynı satıra
   yazdır.
5. 2024'ün ilk yarısının 2023'ün ilk yarısına göre yüzde kaç yüksek olduğunu
   bir ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
2023-07-24
2024-06-28
44299 50659
14.4
```

2024 aynı eşiğe yaklaşık dört hafta erken ulaştı. Birikimli toplam, günlük
inip çıkmaları silip iki yılın farkının nasıl açıldığını gösteriyor.
