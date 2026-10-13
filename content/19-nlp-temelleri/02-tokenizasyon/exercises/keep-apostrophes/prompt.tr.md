`tokenize(text)` "can't" ve "it's" gibi kelimeleri tek token olarak tutsun:
desen `\w+(?:'\w+)?|[^\w\s]`. Metni küçük harfe çevirme; olduğu gibi
parçala.

**Beklenen çıktı:**

```
I|can't|believe|it's|here|!
Don't|stop|.
```
