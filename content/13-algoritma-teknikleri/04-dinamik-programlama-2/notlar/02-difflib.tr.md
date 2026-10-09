Benzer metinleri bulmak için her seferinde düzenleme uzaklığını kendin
yazmak zorunda değilsin. Python'un standart kütüphanesindeki `difflib`
modülü iki metnin ne kadar benzediğini ölçer ve en yakın eşleşmeleri bulur.

```python
import difflib

words = ["pandas", "numpy", "python", "matplotlib", "seaborn", "sklearn"]
print(difflib.get_close_matches("pyhton", words))
print(difflib.get_close_matches("matplot", words, n=1))
print(round(difflib.SequenceMatcher(None, "kitten", "sitting").ratio(), 3))

old = ["import pandas", "df = pandas.read_csv('a.csv')", "print(df.head())"]
new = ["import pandas as pd", "df = pd.read_csv('a.csv')", "print(df.head())"]
for line in difflib.unified_diff(old, new, lineterm="", n=0):
    print(line)
```

```text
['python']
['matplotlib']
0.615
--- 
+++ 
@@ -1,2 +1,2 @@
-import pandas
-df = pandas.read_csv('a.csv')
+import pandas as pd
+df = pd.read_csv('a.csv')
```

- `get_close_matches(kelime, liste)` benzerliği 0,6'dan büyük olanları en
  benzerden başlayarak verir; "bunu mu demek istediniz?" için hazır.
- `SequenceMatcher(...).ratio()` 0 ile 1 arasında benzerlik oranı:
  `2 × eşleşen / toplam uzunluk`.
- `unified_diff` iki metin listesinin farkını `git diff` biçiminde yazar.

`difflib` düzenleme uzaklığı değil, eşleşen en uzun parçaları arayan başka
bir yöntem (Ratcliff–Obershelp) kullanır; sonuçlar çoğu zaman benzer ama
birebir aynı değildir. Büyük veri setlerinde yazım farkı olan kayıtları
eşlemek için `rapidfuzz` gibi C ile yazılmış üçüncü taraf paketler de var.
