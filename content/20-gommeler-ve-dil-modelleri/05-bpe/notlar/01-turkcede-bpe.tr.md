Türkçe sondan eklemeli bir dil: tek bir kökten "evler", "evlerde",
"evlerimizden" gibi yüzlerce biçim türer. Kelime düzeyinde her biçim ayrı bir
kelime; çoğu nadir görülür. BPE'nin ekleri kendiliğinden bulup bulamadığını
dersteki `learn_bpe` ve `encode` ile küçük bir kelime listesinde deneyelim:

```python
words = Counter({"ev": 30, "evler": 20, "evlerde": 8, "evlerden": 6,
                 "evimiz": 5, "kitap": 25, "kitaplar": 15, "kitaplarda": 6,
                 "kitaplardan": 5, "okul": 20, "okullar": 12, "okullarda": 7,
                 "okuldan": 6, "kalem": 15, "kalemler": 10, "kalemlerden": 4})
turkish = learn_bpe(words, 24)
for start in range(0, 24, 4):
    print(turkish[start:start + 4])
for word in ["evlerimizden", "okullardan", "kalemlerde", "masalar"]:
    print(word, encode(word, turkish))
```

```text
[('l', 'e'), ('e', 'v'), ('r', '</w>'), ('t', 'a')]
[('ta', 'p'), ('k', 'i'), ('ki', 'tap'), ('u', 'l')]
[('o', 'k'), ('ok', 'ul'), ('l', 'a'), ('r', 'd')]
[('ev', 'le'), ('ev', '</w>'), ('le', 'm'), ('k', 'a')]
[('ka', 'lem'), ('la', 'r</w>'), ('kitap', '</w>'), ('n', '</w>')]
[('okul', '</w>'), ('evle', 'r</w>'), ('rd', 'e'), ('rd', 'a')]
evlerimizden ['evle', 'r', 'i', 'm', 'i', 'z', 'd', 'e', 'n</w>']
okullardan ['okul', 'la', 'rda', 'n</w>']
kalemlerde ['kalem', 'le', 'rde', '</w>']
masalar ['m', 'a', 's', 'a', 'lar</w>']
```

- İlk kurallar kökleri kuruyor ("kitap", "okul", "kalem"): bu listede en sık
  harf dizileri onlar.
- Ekler de beliriyor, ama dilbilgisinin böldüğü yerden değil. `lar</w>`
  gerçek bir ek; ama "okullardan" `okul + la + rda + n</w>` diye bölünüyor,
  doğrusu `okul + lar + dan` olurdu. BPE dilbilgisi bilmez, yalnızca sık
  parçaları birleştirir.
- "masalar" kökü listede yok: kök harflere bölünüyor ama `lar</w>` eki
  tanınıyor.
- "evlerimizden" büyük ölçüde harflerine bölündü: "imiz" listede yalnızca
  "evimiz"de geçtiği için kural olmadı. Daha büyük bir külliyatta bu ekler de
  parça olabilir.
- 03. bölümdeki kural tabanlı ek ayırmanın aksine, BPE yanlış yerden
  bölebilir; ama dile özgü kural yazmayı gerektirmez ve her dilde aynı
  yöntemle çalışır.
