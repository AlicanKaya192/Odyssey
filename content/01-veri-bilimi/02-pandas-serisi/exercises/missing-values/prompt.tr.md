Altı günlük sıcaklık ölçümünün ikisi yapılamamış. Önce eksiği
**göreceksin**, sonra dolduracaksın.

**Yapman gerekenler:**

1. `temps` serisi başlangıç kodunda hazır, içinde iki `None` var.
2. Kaç ölçümün eksik olduğunu bul, `missing` değişkeninde tut.
3. Ortalamayı hesapla, `average` değişkeninde tut.
4. Eksikleri ortalamayla doldurulmuş yeni bir seri üret, adı `filled` olsun.
5. Sırayla yazdır: `missing`, `temps.count()` ile `temps.size` **yan yana**,
   ortalama (iki basamağa yuvarlanmış), ve `filled` serisinin liste hâli.

**Beklenen çıktı:**

```
2
4 6
25.5
[21.0, 25.5, 24.0, 25.5, 27.0, 30.0]
```

**Asıl ders ikinci satırda.** `count()` dolu hücreleri, `size` hepsini
sayıyor; ikisi farklıysa veride boşluk var demektir.

pandas ortalamayı alırken eksikleri **kendiliğinden atlıyor** — NumPy'da
`nan` alıyordun ve `nanmean` demek zorundaydın. Kolaylık gibi görünüyor ama
kaç kaydın boş olduğunu fark etmemene de yol açabiliyor. Bu yüzden önce
sayıyorsun.
