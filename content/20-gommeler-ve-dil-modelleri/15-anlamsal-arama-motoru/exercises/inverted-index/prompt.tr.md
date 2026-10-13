Arama motorlarının temel yapısı ters dizindir: kelime → içinde geçtiği
belgelerin numaraları. `build_index(docs)` her kelime için numara listesini
(küçükten büyüğe, tekrarsız) kursun; `search_all(index, query)` sorgunun
**bütün** kelimelerini içeren belgelerin numaralarını sıralı döndürsün.

**Beklenen çıktı:**

```
[0, 1] [0, 2]
[0]
[]
```
