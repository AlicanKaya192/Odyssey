Altı kaydın şehir bilgisi elinde. Bir veriyi ilk kez açtığında kategorik
sütuna sorulacak ilk soru budur: **hangisinden kaç tane var?**

**Yapman gerekenler:**

1. `cities` serisi başlangıç kodunda hazır.
2. Her şehirden kaç tane olduğunu hesapla, `counts` adlı seride tut.
3. Sırayla yazdır: `counts`, kaç **farklı** şehir olduğu, ve **en çok tekrar
   eden** şehrin adı.

**Beklenen çıktı:**

```
Ankara    3
Izmir     2
Bursa     1
Name: count, dtype: int64
3
Ankara
```

`Name: count` satırı pandas'ın kendi eklediği bilgi — sonucun ne olduğunu
söylüyor. Onu sen yazmıyorsun.
