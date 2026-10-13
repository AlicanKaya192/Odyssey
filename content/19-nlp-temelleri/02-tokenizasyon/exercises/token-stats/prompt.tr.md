`token_stats(n)` ilk `n` yorumu (küçük harfle) üç parçalayıcıyla parçalasın:
`str.split`, `re.findall(r"\w+|[^\w\s]", ...)` ve scikit-learn'ün
`analyze`'ı. Her biri için `[toplam token, farklı token]` listesi, üçü bir
liste içinde, bu sırayla döndürülsün.

**Beklenen çıktı:**

```
split 31171 519
regex 38001 365
sklearn 30080 350
```
