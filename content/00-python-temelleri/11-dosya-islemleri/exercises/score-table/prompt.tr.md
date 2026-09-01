Yanına `scores.txt` adında bir dosya konuldu. Her satırda bir isim ve bir
not virgülle ayrılmış duruyor; arada bir boş satır var.

```
Ada,90
Alan,70

Grace,85
Brian,60
```

**Yapman gerekenler:**

1. Dosyayı oku ve `scores` adında bir sözlük kur: anahtar isim, değer
   **sayı** olarak not. Boş satırları atla.
2. `average` adında bir değişkende notların ortalamasını **tam bölme** ile
   tut: `sum(...) // len(...)`
3. `top` adında bir değişkende en yüksek notu alan kişinin **adını** tut.
4. Sırayla `scores`, `average` ve `top` yazdır.

**Beklenen çıktı:**

```
{'Ada': 90, 'Alan': 70, 'Grace': 85, 'Brian': 60}
76
Ada
```

Dikkat: dosyadan okunan her şey **metin** olarak geliyor. `"90"` bir sayı
değil; `int()` ile çevirmen gerekiyor.

> Bir satırı ikiye bölmek için `line.split(",")` kullanıyorsun. En yüksek
> değeri taşıyan anahtarı bulmak için sözlükte dolaşıp karşılaştırabilirsin.
