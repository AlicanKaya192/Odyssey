`split_sentences(text)` önce dersteki gibi `re.split(r"(?<=[.!?])\s+", text)`
ile bölsün. Sonra parçaları sırayla dolaşsın: bir önceki cümlenin **son
kelimesi** (küçük harfle) `ABBREVIATIONS` içindeyse yeni parçayı ona bir
boşlukla eklesin, değilse yeni cümle olarak listeye koysun.

**Beklenen çıktı:**

```
Dr. Lee paid $4.50 today.
Great service!
Ask Mr. Kim, e.g. by mail.
Done?
```
