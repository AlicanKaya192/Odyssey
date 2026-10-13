`clean_tokens(text)` sırayla:

1. HTML varlıklarını çözsün (`html.unescape`),
2. etiketleri (`<...>`) boşlukla değiştirsin,
3. küçük harfe çevirip `re.findall(r"[a-z']+", ...)` ile parçalasın,
4. `STOP` kümesindeki kelimeleri atsın.

"not" durak listesinde değil: duygu için korunuyor.

**Beklenen çıktı:**

```
['lid', 'not', 'tight', 'leaks']
```
