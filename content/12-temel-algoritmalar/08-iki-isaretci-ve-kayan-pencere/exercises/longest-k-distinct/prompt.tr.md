`longest_k_distinct(text, k)` fonksiyonunu **değişken pencereyle** yaz:
metinde **en fazla `k` farklı harf** içeren en uzun ardışık parçanın
uzunluğunu döndürsün.

- `longest_k_distinct("eceba", 2)` → `3` (`"ece"`)
- `longest_k_distinct("aaabbcc", 2)` → `5` (`"aaabb"`)

Penceredeki harflerin sayısını bir sözlükte tut. Sağ ucu ilerlet; farklı
harf sayısı `k`'yi geçince soldan çıkar (sayacı sıfıra inen harfi sözlükten
sil) ve sol ucu ilerlet.

**Beklenen çıktı:**

```
3
5
0
```
