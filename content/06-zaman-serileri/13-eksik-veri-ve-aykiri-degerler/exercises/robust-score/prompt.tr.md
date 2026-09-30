Web trafiğinde aykırı günleri önce z-skoruyla, sonra ortanca ve MAD'ye
dayanan dayanıklı puanla ara.

**Yapman gerekenler:**

1. Ortalamayı (bir ondalık), ortancayı ve standart sapmayı (bir ondalık) aynı
   satıra yazdır.
2. z-skorunu hesapla; mutlak değeri 3'ü aşan günleri `"%m-%d"` listesi olarak
   yazdır.
3. `robust(x)` adında bir fonksiyon yaz:
   `0.6745 * (x - x.median()) / (x - x.median()).abs().median()` döndürsün.
4. MAD'yi (ortancadan mutlak sapmaların ortancası) bir ondalığa yuvarlayıp
   yazdır.
5. Dayanıklı puanın mutlak değerce en büyük 5 gününü `"%m-%d"` listesi olarak
   ve puanlarını (bir ondalık, mutlak değer) ayrı bir liste olarak yazdır.
6. 8 Ekim (kesinti günü) için z-skorunu ve dayanıklı puanı iki ondalığa
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
4081.1 4002.0 914.2
['03-14', '06-20', '10-08']
337.5
['03-14', '06-20', '10-08', '11-12', '11-14']
[11.2, 9.8, 7.7, 3.7, 3.5]
-4.31 -7.72
```

İki yöntem de aynı üç günü en üste koyuyor, ama dayanıklı puanda çok daha
belirginler: kesinti günü z-skorunda −4.3, dayanıklı puanda −7.7. Neden?
Standart sapma (914) o üç günün kendisi tarafından şişirilmiş; MAD (337.5)
onlardan etkilenmiyor.
