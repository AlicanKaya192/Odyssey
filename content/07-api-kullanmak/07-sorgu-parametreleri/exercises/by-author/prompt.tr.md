Orwell'ın kitaplarını iste; süzmeyi sunucu yapsın.

**Yapman gerekenler:**

1. `/books` adresine `params={"author": "Orwell"}` ile istek gönder.
2. Giden adresi (`r.url`) yazdır.
3. Kitapların başlıklarını `titles` listesine topla ve her birini bir
   satırda yazdır.

**Beklenen çıktı:**

```
http://api.odyssey.test/books?author=Orwell
Nineteen Eighty-Four
Animal Farm
Homage to Catalonia
```
