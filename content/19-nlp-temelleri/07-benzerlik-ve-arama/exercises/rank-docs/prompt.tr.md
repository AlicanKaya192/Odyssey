`rank(query)` `DOCS` ile bir `TfidfVectorizer` kursun, sorguyu dönüştürsün ve
belgelerin indekslerini kosinüse göre büyükten küçüğe döndürsün. Puanı 0
olan belgeler listeye **girmesin**. Eşitlikte sıra karışmasın diye
`np.argsort(..., kind="stable")[::-1]`.

**Beklenen çıktı:**

```
[2, 3, 0]
[1]
[]
```
