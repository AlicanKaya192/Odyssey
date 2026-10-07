Le Guin'in kitaplarını iç içe kaynak adresinden al. Yazarın numarasını bilmiyorsun;
önce yazar listesinden bul.

**Yapman gerekenler:**

1. `GET /authors` ile yazarları al ve adı `Le Guin` olanın kimliğini
   `author_id` değişkenine koy.
2. `GET /authors/<author_id>/books` ile kitaplarını iste.
3. Kimliği, kitap sayısını ve yıllarıyla başlıkları yazdır.

**Beklenen çıktı:**

```
author id: 6
books: 4
1974 The Dispossessed
1969 The Left Hand of Darkness
1968 A Wizard of Earthsea
1971 The Lathe of Heaven
```
