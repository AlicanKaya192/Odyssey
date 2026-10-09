`huffman_bits(text)` fonksiyonunu yaz: metin Huffman koduyla yazılınca
toplam kaç bit tutacağını döndürsün. Kodları kurmana gerek yok: her
birleştirmede iki grubun sayıları toplamı kadar bit eklenir.

1. Harfleri say (`collections.Counter` serbest), sayıları bir heap'e koy.
2. Heap'te birden çok sayı varken en küçük iki sayıyı çıkar, toplamlarını
   sonuca ekle ve toplamı heap'e geri koy.

Boş metin `0`; tek çeşit harften oluşan metinde her harf 1 bit sayılır.

**Beklenen çıktı:**

```
23
21
4
```
