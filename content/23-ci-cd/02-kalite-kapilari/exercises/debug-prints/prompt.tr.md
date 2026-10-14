Hata ayıklarken eklenip unutulan `print` satırları sık görülen bir lint kuralıdır.

`find_prints(source)` fonksiyonunu yaz: başındaki boşluklar atıldığında `print(` ile **başlayan** satırların numaralarını (1'den) bir listede döndür.

- `line.strip()` satırın başındaki ve sonundaki boşlukları atar.
- `metin.startswith("print(")` metin `print(` ile başlıyorsa `True` verir.

Yorum satırındaki `# print(...)` sayılmaz: o satır `#` ile başlıyor.

**Beklenen çıktı:**

```
[5, 9]
[]
```
