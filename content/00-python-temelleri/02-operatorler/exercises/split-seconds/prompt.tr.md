Bir işlem `200000` saniye sürmüş. Bunu gün, saat, dakika ve saniyeye ayır:

```
2 days 7 hours 33 minutes 20 seconds
```

Dört değişken olsun: `days`, `hours`, `minutes`, `seconds`.

Yalnızca `//` (tam bölme) ve `%` (kalan) ile yapılıyor. Bir gün
`24 * 60 * 60 = 86400` saniye, bir saat `3600` saniye, bir dakika `60`
saniye.

Yol şöyle: önce kaç **tam gün** sığdığını bul. Günler çıkınca geriye kalan
saniyelerle (kalan!) kaç tam saat sığdığını bul. Aynısını dakika için
yap; en son kalan, saniyedir.

> Dikkat: `hours` toplamdaki bütün saatler değil (o 55 olurdu), günler
> çıktıktan sonra **artan** saatler. Her adımda bir öncekinin kalanıyla
> çalış.
