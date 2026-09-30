Kampanyanın ve tatilin etkisini, her olay gününü bir hafta önceki ve sonraki
**aynı günle** karşılaştırarak ölç.

**Yapman gerekenler:**

1. `effect(flag)` adında bir fonksiyon yaz. `flag`, `"promo"` ya da
   `"holiday"`. O sütunun 1 olduğu her gün için:
   - 7 gün öncesini ve 7 gün sonrasını al.
   - Bunlardan indekste **olan** ve o gün ne kampanya ne tatil olanları tut.
   - En az bir komşu kaldıysa, günün satışı eksi komşuların ortalamasını bir
     listeye ekle.
   Fonksiyon, listenin ortalamasını (bir ondalık) ve eleman sayısını demet
   olarak döndürsün.
2. `effect("promo")` ve `effect("holiday")` sonuçlarını alt alta yazdır.
3. Karşılaştırma için kaba etkileri yazdır: her bayrak için, bayrağın 1
   olduğu günlerin ortalaması eksi 0 olduğu günlerin ortalaması (bir ondalık,
   aynı satırda; önce kampanya).

**Beklenen çıktı:**

```
(50.8, 84)
(-76.2, 41)
57.0 -67.3
```

Adil karşılaştırmada kampanya +51, tatil −76. Kaba hesap kampanyayı fazla,
tatili eksik gösteriyordu: kampanyalar hafta içinin yoğun günlerine, tatiller
ise satışın zaten yüksek olduğu sıcak aylara denk geliyor. Gerçek değerler
(veri böyle üretildi) +48 ve −75.
