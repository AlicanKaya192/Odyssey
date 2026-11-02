`phishing_score(mail, weights, threshold)` bir e-postanın uyarı puanını
hesaplasın: `mail`'de değeri `True` olan her işaretin `weights`'teki puanı
toplanır. `mail`'de olmayan işaret `False` sayılır.

`(puan, karar)` demeti döndür: puan `threshold`'a eşit ya da büyükse karar
`"report"`, değilse `"ok"`.

**Beklenen çıktı:**

```
(5, 'report')
(0, 'ok')
```
