`mark_repeats(calls)` her araç çağrısı için `"run"` ya da `"repeat"`
yazsın: aynı çağrı (`json.dumps(call, sort_keys=True)` aynıysa) daha önce
geldiyse `"repeat"`. Anahtar sırası farklı ama içeriği aynı çağrı da
tekrardır.

**Beklenen çıktı:**

```
['run', 'run', 'repeat', 'repeat']
```
