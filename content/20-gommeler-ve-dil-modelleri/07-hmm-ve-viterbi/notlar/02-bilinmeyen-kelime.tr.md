Eğitimde hiç görülmemiş bir kelime gelirse ne olur? Yayım olasılığı bütün
etiketler için aynı küçük değer (düzgünleştirme), yani kelimenin kendisi
hiçbir şey söylemiyor. Karar tamamen geçişlere kalıyor:

```python
for text in ["the zebra was quiet", "they zebra the dog", "a quiet zebra"]:
    print(text, viterbi(text.split()))
```

```text
the zebra was quiet ['DET', 'NOUN', 'VERB', 'ADJ']
they zebra the dog ['PRON', 'VERB', 'DET', 'NOUN']
a quiet zebra ['DET', 'ADJ', 'NOUN']
```

- "zebra" DET'ten sonra isim, PRON'dan sonra fiil etiketi aldı. Model
  kelimeyi hiç görmedi ama cümledeki **yerinden** türünü tahmin etti.
- İnsanlar da böyle yapar: "the glorp was quiet" cümlesindeki "glorp"un
  isim olduğunu biliriz.
- Gerçek etiketleyiciler bilinmeyen kelime için kelimenin **biçimine** de
  bakar: "-ly" ile biten çoğunlukla zarf, "-ing" ile biten fiil, büyük harfle
  başlayan özel isim. HMM'den sonra gelen yöntemler (koşullu rastgele
  alanlar, CRF; sonra sinir ağları) bu tür özellikleri ve daha uzun bağlamı
  birlikte kullanır.
