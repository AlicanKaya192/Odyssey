`delete(node, value)` fonksiyonunu yaz: değeri ağaçtan silsin ve alt ağacın
kökünü döndürsün. Değer yoksa ağaç değişmesin. Üç durum:

- yaprak: çıkar
- tek çocuk: çocuk yerine geçer
- iki çocuk: yerine **sağ alt ağacın en küçüğü** yazılır, sonra o değer sağ
  alt ağaçtan silinir (`minimum` hazır)

`after(values, removed)` ağacı kurup değerleri siliyor, `inorder` sonucunu
ve kökü döndürüyor.

**Beklenen çıktı:**

```
[[1, 4, 6, 8, 10, 13], 8]
[[1, 3, 6, 10, 14], 10]
[[], None]
```
