10'dan ucuz klasikleri istiyorsun ama sunucu fiyata göre süzemiyor
(`price_max` yok). Sunucunun yapabildiği kadar daralt, kalanını Python'da süz.

**Yapman gerekenler:**

1. **Tek bir istekle** `tag=classic` ve `per_page=20` gönder.
2. Gelen kitaplardan fiyatı 10'dan küçük olanları `cheap` listesine al
   (sözlüklerin kendisi).
3. Bunları fiyata göre sıralayıp başlık ve fiyatla yazdır; sonda kaç kitap
   olduğunu yaz.

**Beklenen çıktı:**

```
Animal Farm 6.9
Dubliners 7.8
Persuasion 8.75
Sense and Sensibility 9.1
Mrs Dalloway 9.3
Nineteen Eighty-Four 9.5
To the Lighthouse 9.8
Dune 9.99
cheap classics: 8
```

Kontrol yalnızca **bir** istek atıldığına da bakıyor: her kitap için ayrı
istek atma.
