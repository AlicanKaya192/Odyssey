`details(text)` metindeki sayıları (`9:00` gibi saatler dahil) ve büyük harfle
başlayan kelimeleri bulduğu sırayla döndürsün; ama cümlenin **ilk
kelimesini** (sonundaki `,` ya da `.` atılmış hâliyle) listeye koymasın.
Düzenli ifade: `r"\d+(?::\d+)?|[A-Z][a-z]+"`.

**Beklenen çıktı:**

```
['Monday', 'Friday', '9:00', '17:00']
['Canada', '10']
```
