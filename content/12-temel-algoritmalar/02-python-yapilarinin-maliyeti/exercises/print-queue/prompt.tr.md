Bir yazıcıya işler sırayla geliyor. Yazıcı her turda sıradaki işin
**en fazla 2 sayfasını** basıyor; iş bitmediyse kalan sayfalarıyla kuyruğun
**sonuna** geçiyor.

`print_order(jobs)` fonksiyonunu yaz: `jobs` `[ad, sayfa]` çiftlerinden
oluşan bir liste; fonksiyon işlerin **bittiği sırayla** adlarını döndürsün.

- `[["a", 3], ["b", 1], ["c", 2]]` → `["b", "c", "a"]`
  (a 2 sayfa basıp sona geçer, b ve c biter, a'nın kalan 1 sayfası basılır)

**Kurallar:** kuyruk için `collections.deque` kullan; listede `pop` ve
`insert` kullanma (baştan çıkarmak listede `O(n)`).

**Beklenen çıktı:**

```
['b', 'c', 'a']
['memo', 'report']
```
