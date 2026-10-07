`books.json` bir kitap API'sinin `/books` yanıtı. Kayıtlar `data`
anahtarında, sayfa bilgisi `meta` içinde.

**Yapman gerekenler:**

1. Kayıt listesini `items` değişkenine al.
2. Kayıtların kimliklerini `ids` adlı bir listede topla.
3. Elindeki kayıt sayısını, toplam kayıt sayısını (`meta.total`), kimlikleri
   ve verinin tamamını almak için kaç sayfa gerektiğini yazdır.

Sayfa sayısı: toplamı sayfa boyuna (`per_page`) böl, **yukarı yuvarla**.
Tam sayı aritmetiğiyle: `(total + per_page - 1) // per_page`.

**Beklenen çıktı:**

```
on this page: 5
total: 23
ids: [1, 2, 3, 4, 5]
pages needed: 5
```
