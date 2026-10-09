Ters sayım (`i < j` ama `items[i] > items[j]` olan ikili sayısı) iç içe
döngüyle `O(n²)`. Merge sort ile `O(n log n)`'de sayılabilir:
birleştirirken sağdan bir eleman soldakilerden önce alındığında, **soldaki
kalan bütün elemanlar** ondan büyüktür; hepsi birer ters sayımdır.

`sort_and_count(items)` fonksiyonunu yaz: `(sıralı_liste, ters_sayım)`
demetini döndürsün.

- Temel durum: 0 ya da 1 eleman → `(items, 0)`.
- İki yarının sonuçlarını al: `(left, a)` ve `(right, b)`.
- Birleştirirken `right[j] < left[i]` ise `count += len(left) - i`.
- Sonuç: `(birleşmiş, a + b + count)`.

**Hız şartı:** kodun sonunda 50 000 elemanlı karışık bir liste sayılıyor;
iç içe döngü süreye yetişmez.

**Beklenen çıktı:**

```
([1, 2, 3, 4, 5], 3)
([1, 2, 3, 4, 5], 10)
622355072
```
