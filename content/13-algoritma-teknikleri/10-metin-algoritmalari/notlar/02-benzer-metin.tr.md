İki metin ne kadar benziyor? Kopya ya da tekrarlanan belge bulmanın ilk adımı
metni **parçalara (shingle)** bölmek: art arda gelen `k` kelime. İki metnin
parça kümelerinin **Jaccard benzerliği** = ortak parça / toplam farklı parça.

```python
def shingles(text, k=3):
    words = text.lower().split()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


a = "the model was trained on a large text corpus"
b = "the model was trained on a small text corpus"
sa, sb = shingles(a), shingles(b)
print(len(sa), len(sb), len(sa & sb))
print(round(len(sa & sb) / len(sa | sb), 2))
```

```text
7 7 4
0.4
```

Tek kelime değişti ama o kelimeyi içeren üç parça da değişti; benzerlik 0.4.
`k` küçükse alakasız metinler de ortak parça bulur, büyükse küçük bir değişiklik
benzerliği çok düşürür.

Parçalar Python'da kümeye konunca arka planda zaten hash'leniyor; Rabin-Karp'ın
kayan hash'i bunu harf düzeyinde hızlı yapmanın yolu. Milyonlarca belgede her
çifti karşılaştırmak ise mümkün değil: bölüm 13'teki **MinHash** her kümeyi
birkaç sayılık bir imzaya indirip Jaccard'ı tahmin ediyor.
