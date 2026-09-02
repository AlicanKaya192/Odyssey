Bu, ders anlatımındaki on satırlık örneğin kendisi. Bir kez elle
yazdığında `groupby` sana bir daha sihir gibi gelmeyecek.

**Yapman gerekenler:**

1. `records` listesi başlangıç kodunda hazır.
2. Her şehir için not **ortalamasını** hesapla ve sonucu `averages` adlı bir
   sözlükte tut. Anahtar şehir adı, değer ortalama olacak.
3. Şehirleri **alfabetik sırayla** dolaş ve her satırda şehir adını ve
   ortalamasını yazdır.

**Beklenen çıktı:**

```
Ankara 83.0
Bursa 88.0
Izmir 71.0
```

**İpucu:** iki sözlükle ilerlemek en kolayı — biri toplam, biri sayaç.

pandas'ta bu tek satır olacak: `data.groupby("city")["score"].mean()`
