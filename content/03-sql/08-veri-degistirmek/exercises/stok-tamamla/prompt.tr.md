Stoğu **5'in altında** olan ürünlerin stoğunu `20` yap.

Dört ürün etkilenecek. Diğerlerinin stoğu değişmemeli.

Bu alıştırmanın asıl konusu komut değil, **alışkanlık**. Yazmadan önce
provasını yap:

```sql
SELECT * FROM products WHERE stock < 5;
```

Ekranda hangi satırların değişeceğini gör. Dört satır geldiyse `WHERE`
doğru demektir; şimdi aynı `WHERE` ile `UPDATE` yazabilirsin.

İki saniye sürüyor ve `UPDATE` yazarken yapılan hataların neredeyse
hepsini engelliyor. Gerçek bir veritabanında geri alma düğmesi yok.
