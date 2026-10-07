Paralel işin ilk adımı işi parçalara bölmek. Bir aralığı eşit parçalara
bölen bir fonksiyon yaz.

**Yapman gerekenler:**

`split_range(n, parts)` fonksiyonunu yaz. 0'dan `n`'ye kadar olan aralığı
`parts` parçaya bölüp `(başlangıç, bitiş)` demetlerinin listesini döndürsün:

- Parça genişliği `size = n // parts`.
- `i`. parça `(i * size, (i + 1) * size)`.
- **Son parçanın bitişi her zaman `n`**: bölüm tam değilse artan kısım son
  parçaya eklensin.

Örnekler:

- `split_range(100, 4)` → `[(0, 25), (25, 50), (50, 75), (75, 100)]`
- `split_range(10, 3)` → `[(0, 3), (3, 6), (6, 10)]`
