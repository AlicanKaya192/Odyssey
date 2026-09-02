Grup ortalaması **tek başına** okunmuyor. Bu alıştırma sebebini
gösteriyor.

**Yapman gerekenler:**

1. Şehre göre grupla ve `score` için **hem sayı hem ortalama** hesapla; tek
   ondalığa yuvarla.
2. Tabloyu yazdır.
3. **En küçük grubun** kaç kişilik olduğunu yazdır.
4. Ortalaması **en yüksek** şehri yazdır.
5. Ortalaması **en düşük** şehri yazdır.

**Beklenen çıktı:**

```
        count  mean
city
Ankara      4  76.5
Bursa       2  48.0
Izmir       4  81.5
2
Izmir
Bursa
```

**Çıktıya bak:** Bursa'nın ortalaması 48, diğerlerinin 76 ve 81. Fark
büyük görünüyor.

Ama `count` sütununda Bursa'nın yanında **2** yazıyor. İki kişilik bir
grubun ortalaması hakkında söylenebilecek bir şey yok — bir kişi eksik ya
da fazla olsa sayı tamamen değişirdi.

`agg(["count", "mean"])` yazmanın sebebi bu. Ortalamayı tek başına
isteseydin bu tuzağı göremezdin.

Raporda bu şöyle yazılıyor: "Bursa'daki iki kayıt düşük" — "Bursa'da notlar
düşük" değil.
