Düzey kaymasını CUSUM ile yakala ve kırpmanın, payın ve eşiğin etkisini gör.

Başlangıç kodunda `z` hazır: Ocak–Şubat referansına göre standartlaştırılmış
oransal sapma (kırpılmamış).

**Yapman gerekenler:**

1. `cusum(z, k, h)` fonksiyonunu yaz. Toplam sıfırdan başlar; her gün
   `total = max(0, total + değer - k)`. Toplam `h`'yi geçerse o gün alarm
   listesine eklenir ve toplam **sıfırlanır**. Alarm günlerinin listesini
   döndürsün.
2. Kırpılmış seriyle (`z.clip(-3, 3)`), `k = 1`, `h = 8`: ilk alarm gününü
   (`"%Y-%m-%d"`), bu günün 2 Eylül'den kaç gün sonra olduğunu ve toplam alarm
   sayısını aynı satıra yazdır.
3. Kırpılmamış `z` ile aynı ayarlarda ilk alarm gününü yazdır.
4. Kırpılmış seriyle `k = 0.5`, `h = 5`: 2 Eylül'den **önceki** alarm günlerini
   `"%m-%d"` listesi olarak yazdır.

**Beklenen çıktı:**

```
2024-09-05 3 23
2024-03-14
['03-11', '05-10', '06-13']
```

Kırpılmış CUSUM sekiz ay sessiz kalıyor ve kaymayı üç gün sonra yakalıyor. Ama
referans güncellenmediği için yıl sonuna kadar çalmaya devam ediyor: alarm
"referansı yenile" demek. Kırpılmazsa 14 Mart'taki tek kampanya günü eşiği
tek başına aşıyor. Daha duyarlı ayar (`k = 0.5`, `h = 5`) Eylül'den önce üç
yanlış alarm veriyor.
