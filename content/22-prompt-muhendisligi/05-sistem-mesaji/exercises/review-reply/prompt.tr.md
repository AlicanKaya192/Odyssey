`review(reply, max_sentences)` dersteki üç kuralı denetlesin ve bulduğu
sorunları bu sırayla döndürsün: cümle sayısı (`re.split(r"[.!?]+", reply)`,
boş parçalar sayılmaz) `max_sentences`'ı geçiyorsa `"too long"`; hazır
`PROMISE` kalıbı bulunuyorsa `"promise"`; büyük/küçük harfe bakmadan
`as an ai` kelimeleri geçiyorsa (`r"\bas an ai\b"`)
`"talks about itself"`.

**Beklenen çıktı:**

```
['promise']
['too long']
['talks about itself']
```
