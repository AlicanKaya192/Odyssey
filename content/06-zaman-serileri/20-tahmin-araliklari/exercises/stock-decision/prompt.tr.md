Her sabah kaç tane üretilmeli? Karşılanamayan her talep 4 birim, satılamayan
her ürün 1 birim zarar.

Başlangıç kodunda `past`, `base` ve `actual` hazır (bir önceki alıştırmadaki
gibi).

**Yapman gerekenler:**

1. `cost(order)` fonksiyonunu yaz. `order`, her gün üretilen miktar (seri):
   - eksik: `(actual - order).clip(lower=0)`
   - fazla: `(order - actual).clip(lower=0)`
   - dört şeyi demet olarak döndür: stokun bittiği gün sayısı, toplam eksik,
     toplam fazla, toplam maliyet (`4 * eksik + 1 * fazla`); hepsi tam sayı.
2. `q = 0.5, 0.8, 0.9, 0.95` için üretim kuralı `base + past.quantile(q)`.
   Her biri için `q` ile birlikte `cost` sonucunu yazdır.
3. Formülün söylediği yüzdeliği hesapla ve yazdır: `4 / (4 + 1)`.
4. Dört kural arasında maliyeti en düşük olanın `q` değerini ve nokta
   tahminine (`q = 0.5`) göre sağladığı tasarruf yüzdesini (tam sayı) aynı
   satıra yazdır.

**Beklenen çıktı:**

```
0.5 (178, 2333, 2730, 12062)
0.8 (73, 609, 6130, 8566)
0.9 (32, 230, 8313, 9233)
0.95 (14, 119, 10032, 10508)
0.8
0.8 29
```

En düşük maliyet formülün söylediği yüzdelikte. Nokta tahmini kadar üretmek
günlerin yarısında stoksuz bırakıyor; aşırı temkin (`q = 0.95`) ise fireyi
büyütüp maliyeti yeniden artırıyor. Aynı tahmin yöntemi, aynı veri: tek fark,
belirsizliğin ve maliyetlerin karara katılması.
