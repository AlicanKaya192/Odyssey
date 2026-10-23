Dersteki `Student` sınıfını yaz: kurucu bir ad ve bina alır. Ad boşsa `ValueError("Missing name")`, bina `Gryffindor`, `Hufflepuff`, `Ravenclaw`, `Slytherin`'den biri değilse `ValueError("Invalid house")` yükseltir; değilse ikisini saklar. `__str__` `Harry from Gryffindor` döndürür. Program adı ve binayı sorup öğrenciyi yazdırır; geçersiz girdide hatayı yakalamaz, program hatayla biter.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```
