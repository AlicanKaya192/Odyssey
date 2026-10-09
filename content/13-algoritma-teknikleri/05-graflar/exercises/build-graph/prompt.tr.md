`build_graph(edges)` fonksiyonunu yaz: `[a, b]` çiftlerinden **yönsüz** bir
komşuluk sözlüğü kursun (düğüm → komşular kümesi). Kenarı **iki yöne de**
ekle; `setdefault` işini kolaylaştırır.

`neighbours(edges)` sonucu karşılaştırılabilir olsun diye sıralı listelere
çeviriyor.

**Beklenen çıktı:**

```
ada ['bora', 'cem']
bora ['ada', 'cem', 'deniz']
cem ['ada', 'bora', 'deniz']
deniz ['bora', 'cem', 'ece']
ece ['deniz', 'fuat']
fuat ['ece']
```
