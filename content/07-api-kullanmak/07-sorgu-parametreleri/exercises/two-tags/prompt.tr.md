Alıştırma sunucusu aynı adı birden çok kez görünce "hepsi olsun" diye
okuyor. Hem `scifi` hem `classic` etiketli kitapları iste, sonra yalnızca
`scifi` olanlarla karşılaştır.

**Yapman gerekenler:**

1. `tag` değerine bir **liste** vererek iki etiketi birlikte iste. Giden
   adresi ve gelen başlıkları yazdır.
2. Yalnızca `tag=scifi` ile iste ve kaç kitap geldiğini (`meta.total`)
   yazdır.

**Beklenen çıktı:**

```
http://api.odyssey.test/books?tag=scifi&tag=classic
Dune
scifi only: 8
```
