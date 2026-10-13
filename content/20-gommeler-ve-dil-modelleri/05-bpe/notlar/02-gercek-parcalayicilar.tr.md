Gerçek modellerin parçalayıcıları bu dersteki BPE'nin akrabaları:

| Yöntem | Fark |
|---|---|
| WordPiece | Çifti sıklığa değil, birleşmenin olasılığı ne kadar artırdığına göre seçer; kelime içi parçalar `##` ile işaretlenir |
| SentencePiece | Metni önceden kelimelere ayırmaz; boşluğu da bir sembol (`▁`) sayar, her dilde aynı çalışır |
| Bayt düzeyi BPE | Harfler yerine 256 bayttan başlar; emoji dahil hiçbir karakter bilinmeyen kalmaz |

## Parça sayısı neden önemli?

Dil modelleri metni parça parça işler: ne kadar metin alabildikleri
(bağlam uzunluğu) ve hesap maliyeti **parça sayısıyla** ölçülür. Bir
parçalayıcı bir dil için eğitildiyse başka dilleri daha çok parçaya böler.
Dersteki İngilizce taleplerle öğrenilmiş `merges` ile birinci notun Türkçe
kelimelerini parçalayalım:

```python
english = [w for w in test for _ in range(test[w])]
turkish_words = ["evlerimizden", "okullardan", "kitaplarda", "kalemler",
                 "evlerde", "okuldan"]
for name, sample in [("english", english), ("turkish", turkish_words)]:
    pieces = sum(len(encode(w, merges)) for w in sample)
    print(name, round(pieces / len(sample), 2))
```

```text
english 1.34
turkish 6.67
```

- İngilizce talepler kelime başına 1,34 parça, Türkçe kelimeler 6,67:
  neredeyse harf harf. Parçalayıcı Türkçe kökleri de ekleri de hiç
  görmedi.
- Bu ölçeklenince önemli bir eşitsizlik: aynı anlamı taşıyan metin bazı
  dillerde çok daha fazla parça tutar; modelin bağlamı daha çabuk dolar,
  işlem daha pahalı olur. Çok dilli modeller bu yüzden parçalayıcılarını
  birçok dilden derlenmiş metinle eğitir.
