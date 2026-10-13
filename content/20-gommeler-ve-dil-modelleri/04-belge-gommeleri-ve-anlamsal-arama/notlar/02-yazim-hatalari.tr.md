Derste "refund"un en yakın komşuları yazım hatalarıydı. Bu ne kadar
yaygın? Veri üreticisi yazım hatası yaparken iki komşu harfin yerini
değiştiriyor; yani hatalı kelime doğrusuyla **aynı harflerden** oluşuyor.
Dersteki `E` ile birkaç kelimenin ilk beş komşusunda bunları sayalım:

```python
for word in ["parcel", "refund", "password", "invoice", "account", "tracking"]:
    sims = E @ E[index[word]]
    top = [vocab[i] for i in np.argsort(-sims)[1:6]]
    typos = [t for t in top if sorted(t) == sorted(word)]
    print(f"{word:<9} {len(typos)} {typos}")
```

```text
parcel    3 ['pracel', 'parecl', 'pacrel']
refund    3 ['rfeund', 'refnud', 'reufnd']
password  3 ['paswsord', 'psasword', 'passwrod']
invoice   4 ['invocie', 'ivnoice', 'invioce', 'inovice']
account   3 ['acconut', 'accuont', 'acocunt']
tracking  4 ['tracikng', 'tracknig', 'trcaking', 'trakcing']
```

- Birçok kelimenin ilk beş komşusunun çoğu kendi yazım hataları. Vektörler
  bunu harflere bakarak değil, **bağlama** bakarak öğrendi: "rfeund" ile
  "refund" aynı cümle kalıplarında geçiyor.
- Bunun için hatalı biçimin eğitimde birkaç kez görülmesi gerekti (dağarcığa
  en az 3 kez geçenleri aldık). Hiç görülmemiş bir yazım hatasının vektörü
  yok.
- Görülmemiş hatalar için kelimeyi **harf parçalarından** kurmak gerekir:
  fastText gibi yöntemler bir kelimenin vektörünü harf n-gram'larının
  vektörlerinin toplamı olarak öğrenir; "pracel" ile "parcel" birçok parçayı
  paylaşır. Bir sonraki bölümdeki BPE de aynı fikrin bir başka biçimi.
