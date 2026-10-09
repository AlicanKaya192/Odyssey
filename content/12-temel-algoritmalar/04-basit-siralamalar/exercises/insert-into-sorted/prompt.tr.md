Eklemeli sıralamanın kalbi tek bir adım: sıralı bir listeye yeni bir değeri
**doğru yerine kaydırarak** yerleştirmek.

`insert_sorted(sorted_items, value)` fonksiyonunu yaz: sıralı listenin bir
kopyasının sonuna `value`'yu ekleyip **sondan başa doğru** kendinden büyük
olanları bir sağa kaydırarak yerine yerleştirsin ve yeni listeyi
döndürsün.

`insert`, `sorted`, `.sort()` ve `bisect` kullanma.

**Beklenen çıktı:**

```
[10, 20, 25, 30, 40]
[5, 10, 20, 30, 40]
[10, 20, 30, 40, 50]
[7]
```
