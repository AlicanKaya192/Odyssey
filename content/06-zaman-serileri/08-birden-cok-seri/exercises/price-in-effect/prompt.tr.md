A mağazasının birim fiyatı yılda birkaç kez değişiyor. `prices.csv`
yalnızca değişiklik günlerini içeriyor (`valid_from`, `price`). Her günün
satışını o gün geçerli olan fiyatla çarpıp ciroyu bul.

**Yapman gerekenler:**

1. `stores.csv` dosyasını oku; A mağazasının `date` ve `sales` sütunlarını
   al ve tarihe göre sırala.
2. `prices.csv` dosyasını `parse_dates=["valid_from"]` ile oku.
3. Önce sıradan birleştirmeyi dene (`merge`, `how="left"`) ve fiyatı dolu
   olan satır sayısını yazdır.
4. `pd.merge_asof` ile birleştir (`left_on="date"`,
   `right_on="valid_from"`). 14, 15 ve 16 Mart 2024 satırlarının fiyatlarını
   liste olarak yazdır.
5. `revenue = sales * price` sütununu ekle ve toplam ciroyu bir ondalığa
   yuvarlayıp yazdır.
6. Her fiyatın kaç gün geçerli olduğunu sözlük olarak yazdır:
   `joined["price"].value_counts().sort_index().to_dict()`.

**Beklenen çıktı:**

```
5
[19.9, 21.5, 21.5]
2562737.2
{19.9: 74, 21.5: 78, 21.9: 71, 22.9: 101, 24.5: 42}
```

Sıradan birleştirme yalnızca fiyatın değiştiği beş günü eşledi.
`merge_asof` her gün için geriye bakıp en son fiyat kaydını buldu: 14 Mart
eski fiyatta, 15 Mart'tan itibaren yeni fiyat geçerli.
