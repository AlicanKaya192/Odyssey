Geçme notu 75'e çekildi: bunun altında kalan herkesin notu 75
yapılacak. Veriyi dosyadan okuyup tabloyu **gerçekten** değiştireceksin.

Veri `students.csv` dosyasında:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**Yapman gerekenler:**

1. İçe aktarmayı yaz ve dosyayı oku.
2. Notu **75'in altında** olanları gösteren bir koşul kur ve bu kişilerin
   adlarını **liste olarak** yazdır.
3. Aynı koşulla bu satırların `score` değerini `75` yap.
4. Kaç kişinin notunun tam 75 olduğunu yazdır.
5. Yeni not ortalamasını (iki ondalık) yazdır.

**Beklenen çıktı:**

```
['Kerem', 'Deniz', 'Kaan', 'Ela', 'Can']
5
79.67
```

**Bu alıştırmanın asıl konusu şu:** aşağıdaki satır **hiçbir şey yapmıyor.**

```python
data[data["score"] < 75]["score"] = 75
```

Köşeli parantez ara bir tablo üretiyor, atama ona gidiyor, o tablo da hemen
çöpe atılıyor. Hata da almıyorsun — kod çalışıyor ve tablo değişmemiş
oluyor. Ortalama 77.42'de kalırdı.

Doğrusu seçimi ve atamayı **tek bir `loc` çağrısında** yapmak:
`data.loc[koşul, "score"] = 75`. Kural: tabloyu değiştireceksen köşeli
parantezi iki kez üst üste kullanma.
