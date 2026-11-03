`lookalikes(names, popular)` `names`'teki her ad için, ad `popular`'da
**yoksa** ve popüler bir ada çok benziyorsa `"<ad> -> <populer>"`
satırını, `names` sırasıyla döndürsün. Benzerlik:
`difflib.get_close_matches(ad, popular, n=1, cutoff=0.8)`. Popüler adın
kendisi ve hiçbir şeye benzemeyen ad listelenmez.

**Beklenen çıktı:**

```
numpi -> numpy
flaskk -> flask
```
