Kuralları tabloya yazılmış bir `parts` tablosu kur.

| Sütun | Tip | Kural |
|---|---|---|
| `id` | `INT` | birincil anahtar |
| `sku` | `NVARCHAR(20)` | boş kalamaz, iki parçada aynı olamaz |
| `price` | `DECIMAL(10,2)` | boş kalamaz, **sıfırdan büyük** |

Yalnızca tabloyu kur, satır ekleme.

Kontrol kuralları **kendisi deniyor**: geçerli bir parça ekliyor, sonra
aynı `sku` ile ikinci bir parça, eksi fiyatlı bir parça ve sıfır fiyatlı
bir parça eklemeye çalışıyor. İlki kabul edilmeli, diğer üçü
reddedilmeli.

Kural uygulamanın kodunda değil tabloda durunca, bu tabloya yazan her
program ona uymak zorunda kalıyor.
