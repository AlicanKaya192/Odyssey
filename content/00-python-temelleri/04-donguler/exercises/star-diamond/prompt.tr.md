`height = 7` için ekrana bu elması çiz:

```
   *
  ***
 *****
*******
 *****
  ***
   *
```

Kurallar:

- Elmas `height` satır; `height` her zaman tek sayı. Kodun `height`'ı 5 ya
  da 9 yapınca da doğru elması çizmeli.
- Çıktı **boşluğu boşluğuna** karşılaştırılıyor: satırların başındaki
  boşluklar şeklin parçası, sonlarında ise boşluk olmamalı.

Önce bir satırı düşün: başta kaç boşluk, sonra kaç yıldız var? Üst yarıda
her satırda yıldız **iki artıyor**, boşluk **bir azalıyor**; alt yarıda
tersi. Satır numarasıyla bu iki sayı arasındaki ilişkiyi bulursan, gerisi
bir döngü.

Bir metni sayıyla çarpınca tekrar eder: `" " * 3` üç boşluk, `"*" * 5` beş
yıldız. İkisini `+` ile birleştirip yazdırabilirsin.

> Dikkat: `print(" " * 3, "*" * 5)` yazarsan virgül araya fazladan bir
> boşluk koyar ve şekil kayar. Parçaları `+` ile birleştir.
