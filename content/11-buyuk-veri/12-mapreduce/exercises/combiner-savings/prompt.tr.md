Beş "makinede" birleştiricinin ağdan geçecek çift sayısını ne kadar
azalttığını ölç.

**Yapman gerekenler:**

1. `orders = make_orders(200_000)`; tabloyu 40 000'lik beş parçaya böl
   (her parça bir makine).
2. Her parçada `(payment, quantity)` çiftlerini kur.
3. Birleştiricisiz: bütün çiftlerin sayısını topla.
4. Birleştiricili: her parçada çiftleri `defaultdict(int)` ile ödeme türü
   başına topla; gönderilecek çift sayısı bu sözlüğün uzunluğu. Ayrıca
   bütün parçaların bu yerel toplamlarını tek bir sözlükte birleştir.
5. İki sayıyı aynı satıra yazdır.
6. Birleştirilmiş toplamların pandas'ın
   `orders.groupby("payment")["quantity"].sum()` sonucuyla aynı olup
   olmadığını yazdır.

**Beklenen çıktı:**

```
200000 15
True
```
