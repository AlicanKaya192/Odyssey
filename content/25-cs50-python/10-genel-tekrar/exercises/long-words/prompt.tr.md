Klasördeki `words.txt`'deki uzun kelimeleri numaralayarak yazan bir program yaz. Program `Minimum length: ` diye bir uzunluk sorsun ve en az o kadar harfli her kelimeyi dosyadaki sırasıyla `1. generators` biçiminde yazsın. Kelimeler boşluklarla ayrılmış; dosyada boş satır da var.

Kelimeleri bulan `long_words(path, length)` bir **üreteç** olsun: dosyayı satır satır okuyup her uygun kelimeyi `yield` ile versin, liste kurmasın. Numaraları `enumerate` ile ver.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Minimum length: 6
1. Python
2. generators
3. values
4. without
5. holding
6. everything
7. memory
```
