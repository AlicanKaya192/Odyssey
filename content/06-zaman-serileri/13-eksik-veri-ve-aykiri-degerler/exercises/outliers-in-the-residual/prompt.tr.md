Ham seride aykırı değer aramak, mevsim ve seviye değişimiyle karışıyor.
Aynı işi dayanıklı STL'in kalıntısında yap ve farkı gör.

Başlangıç kodunda `robust(x)` fonksiyonu hazır.

**Yapman gerekenler:**

1. Çeyrekler arası aralık kuralını **ham seriye** uygula: `q1` ve `q3`
   çeyrekleri, `iqr = q3 - q1`; `q1 - 1.5 * iqr`'nin altında ya da
   `q3 + 1.5 * iqr`'nin üstünde kalan gün sayısını yazdır.
2. Bu günlerden kaçının 2 Eylül'den **sonra** olduğunu yazdır.
3. Dayanıklı STL kur (`STL(visits, period=7, robust=True).fit()`) ve
   kalıntının dayanıklı puanını hesapla.
4. Puanı mutlak değerce en büyük 5 günü `"%m-%d"` listesi olarak ve
   puanlarını (bir ondalık, mutlak değer) ayrı bir liste olarak yazdır.
5. Mutlak puanı 3.5'i aşan ve 20'yi aşan gün sayılarını aynı satıra yazdır.

**Beklenen çıktı:**

```
20
16
['03-14', '10-08', '06-20', '09-24', '12-16']
[50.0, 46.3, 45.4, 12.9, 5.8]
30 3
```

Ham seride kural 20 günü aykırı sayıyor ve çoğu Eylül'den sonra: bunlar
aykırı değer değil, yeni düzeyin sıradan günleri. Kalıntıda üç gün 45–50
puanla her şeyden kopuk. Sabit 3.5 eşiği ise 30 günü işaretliyor: eşik yerine
sıralamaya ve kopmanın yerine bak.
