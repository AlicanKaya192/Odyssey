`employees` tablosundaki `name` sütunu ad ile soyadı birlikte tutuyor:
`Ada Kilic`, `Bora Yilmaz`... İkisini ayrı sütunlara ayır.

Sütunlar: `id`, `first_name`, `last_name`. `id`'ye göre sırala.

```
id  first_name  last_name
--  ----------  ---------
1   Ada         Kilic
2   Bora        Yilmaz
...
```

Adların uzunluğu farklı, o yüzden sabit bir sayı yazamazsın. Önce
boşluğun **nerede** olduğunu bul, sonra ondan önceki ve sonraki parçayı
al.

Boşluğun kendisi iki tarafta da görünmemeli — kontrol, sonunda ya da
başında boşluk kalan bir adı yanlış sayıyor.
