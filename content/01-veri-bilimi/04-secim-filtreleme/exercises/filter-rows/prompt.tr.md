Ankara'da notu 80 ve üstünde olanları bulacaksın.

**Yapman gerekenler:**

1. Şehri `"Ankara"` **ve** notu 80 veya üstünde olan satırları `selected`
   adlı tabloda topla.
2. `selected` tablosunun `name` ve `score` sütunlarını yazdır.
3. Kaç satır seçildiğini yazdır.
4. Seçilenlerin not ortalamasını (iki basamağa yuvarlanmış) yazdır.
5. `selected` tablosunun index'ini liste hâlinde yazdır.

**Beklenen çıktı:**

```
   name  score
0   Ada     82
2  Mina     91
4   Efe     88
3
87.0
[0, 2, 4]
```

**İki tuzak var:**

- `and` **çalışmıyor**; `&` kullanacaksın ve **her koşulu parantez içine**
  alacaksın. Parantezi unutursan `&` karşılaştırmadan önce çalışıyor.
- Son satırda index `[0, 1, 2]` değil `[0, 2, 4]`. Filtre seçilmeyen
  satırların numaralarını **atlıyor**, yeniden numaralamıyor.
