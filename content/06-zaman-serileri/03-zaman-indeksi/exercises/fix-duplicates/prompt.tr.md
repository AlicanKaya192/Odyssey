Bazı günlerin satışı iki parça hâlinde iki ayrı satıra yazılmış. Onları
bul ve birleştir.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku ve sırala.
2. Tekrarlanan tarih sayısını yazdır (`index.duplicated().sum()`).
3. Tekrarlanan tarihleri `"%Y-%m-%d"` biçiminde liste olarak yazdır.
4. 5 Mart 2024'ün değerlerini liste olarak yazdır (`.tolist()`).
5. Parçaları topla: `groupby(level=0).sum()`. Yeni serinin satır sayısını ve
   indeksin tekrarsız olup olmadığını (`is_unique`) aynı satıra yazdır.
6. 5 Mart 2024'ün yeni değerini yazdır.

**Beklenen çıktı:**

```
4
['2024-03-05', '2024-06-18', '2024-09-09', '2024-11-30']
[157, 105]
358 True
262
```

157 ve 105 aynı günün iki parçasıydı; toplamları 262, temiz dosyadaki değer.
Parçalardan birini atsaydın o günün satışı yarıya yakın düşerdi.
