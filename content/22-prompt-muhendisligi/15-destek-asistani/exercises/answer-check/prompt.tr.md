`answer_problems(text, facts)` cevaptaki sorunları sırayla listelesin:
cevaptaki her tarih (`\d{4}-\d{2}-\d{2}`) `facts["date"]`'ten farklıysa
`"date"`; hazır `PROMISE` kalıbı bulunursa `"promise"`; hazır `ACTION`
kalıbı bulunursa `"action"`.

**Beklenen çıktı:**

```
[]
['date', 'promise']
['action']
```
