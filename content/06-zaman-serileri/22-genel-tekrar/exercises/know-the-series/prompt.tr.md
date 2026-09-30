Model kurmadan önce temiz seriye (`bike_clean.csv`) beş soru sor.

Başlangıç kodunda `y` (günlük kiralama) ve `weather` (`temp_c`, `rain`) hazır.

**Yapman gerekenler:**

1. **Büyüyor mu?** Yıllık toplamları (tam sayı listesi) ve yıldan yıla yüzde
   değişimi (bir ondalık, iki değerlik liste) aynı satıra yazdır.
2. **Haftalık desen?** Haftanın günü ortalamalarını (pazartesiden pazara, tam
   sayı listesi) ve cumartesinin pazartesiye oranını (iki ondalık) aynı satıra
   yazdır.
3. **Yıllık desen?** Ay ortalamaları içinde en yüksek ve en düşük ayın
   numarasını ve ikisinin oranını (iki ondalık) aynı satıra yazdır.
4. **Durağan mı?** `adfuller` p-değerini düzey için ve birinci fark için üç
   ondalıkla aynı satıra yazdır.
5. **Dış etken?** Yağmurlu günlerin ortalamasının kuru günlerin ortalamasına
   oranını ve kiralama ile sıcaklık arasındaki korelasyonu (ikisi de iki
   ondalık) aynı satıra yazdır.

**Beklenen çıktı:**

```
[116942, 134269, 149699] [14.8, 11.5]
[329, 343, 343, 353, 366, 443, 383] 1.35
7 1 2.37
0.325 0.0
0.55 0.78
```

Seri yılda yüzde 12–15 büyüyor, hafta sonu yüksek, yazın kışın iki katından
fazla. Düzeyde durağan değil (p = 0.33); farkı alınınca durağan. Ve yağmurlu
bir gün kuru bir günün yarısı kadar: serideki oynamanın en büyük kaynağı,
takvimde yazmayan bir şey.
