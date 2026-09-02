`iloc` ile satır ve sütunları **sıralarına göre** seçeceksin.

**Yapman gerekenler:**

1. İlk satırın ilk sütunundaki değeri yazdır.
2. **1. ve 2. satırların** `name` ve `score` sütunlarını yazdır.
3. Birinci ve üçüncü sütunun **ilk üç satırını** yazdır.
4. **Son satırın** adını yazdır.

**Beklenen çıktı:**

```
Ada
    name  score
1  Kerem     74
2   Mina     91
    name  score
0    Ada     82
1  Kerem     74
2   Mina     91
Sila
```

**Dikkat:** `iloc[1:3]` **iki** satır veriyor — bitiş dâhil değil, Python
kuralı. `loc` böyle davranmıyor; onu bir sonraki alıştırmada göreceksin.
