Derste konular okunur çıktı, çünkü önce durak kelimeleri ve veriye özgü
gürültüyü attık. Aynı NMF'i hiç ön işleme yapmadan çalıştıralım:

```python
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
for name, vectorizer in [
    ("raw", TfidfVectorizer(min_df=5)),
    ("stop", TfidfVectorizer(min_df=5, stop_words="english")),
]:
    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()
    nmf = NMF(n_components=5, random_state=0, max_iter=500).fit(X)
    print(name)
    for row in nmf.components_:
        print(" ", " ".join(words[row.argsort()[::-1][:5]]))
```

```text
raw
  account my to email how
  it ord order got yet
  the app this is page
  box parcel was open damaged
  for ord can of order
stop
  ord order delivered got says
  account address change locked attempts
  app page time history error
  arrived box parcel damaged open
  example com received verification email
```

- **Ham** hâlde konular "my", "to", "the", "it" gibi kelimelerle dolu.
  TF-IDF bu kelimeleri biraz bastırıyor ama tamamen silmiyor; çok sık
  geçtikleri için her konuya sızıyorlar.
- **Hazır durak listesiyle** konular okunur hâle geliyor, ama "ord" (sipariş
  numaraları), "com" ve "example" (e-posta adresleri) gibi bu veriye özgü
  parçalar konuların başına çıkıyor. Bunlar hiçbir genel listede yok; ancak
  konulara bakınca fark ediliyor.

Konu modellemede ön işleme bir kez yapılıp bırakılmaz: konulara bak,
anlamsız kelimeyi durak listesine ekle, yeniden çalıştır. Bu bir döngüdür.
Ama dikkat: konuya göre kelime atmak, sonucu istediğin konulara doğru
itmek demek de olabilir. Neyi neden attığını yaz.
