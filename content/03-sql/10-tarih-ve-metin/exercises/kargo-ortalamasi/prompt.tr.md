Her kargo firması için siparişten kargoya **ortalama kaç gün** geçtiğini
hesapla.

Sütunlar: `carrier`, `avg_days`. `avg_days` virgülden sonra **iki
basamağa** yuvarlanmış olsun. Firma adına göre sırala.

```
carrier   avg_days
--------  --------
CityMove  3.00
FastLine  2.67
NorthWay  3.00
```

Üç tuzak birden var:

- Sipariş tarihi `orders`'ta, kargo tarihi `shipments`'ta: iki tabloyu
  birleştirmen gerekiyor.
- `DATEDIFF`'te sıra önemli: önce erken tarih. Ters yazarsan sonuç eksi.
- `DATEDIFF` tam sayı döndürüyor ve **tam sayıların ortalaması da tam
  sayı**: FastLine için 2,67 yerine 2 çıkıyor. Beşinci bölümdeki tam sayı
  bölmesinin aynısı.
