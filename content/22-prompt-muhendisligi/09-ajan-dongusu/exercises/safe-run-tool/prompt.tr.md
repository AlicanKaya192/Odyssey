Başlangıçtaki `run_tool` bilinmeyen araçta, eksik siparişte ya da yanlış
argümanda **çöküyor**. Onu düzelt: araç `TOOLS`'ta yoksa
`{"error": "unknown tool <ad>"}`; çalıştırırken `TypeError` ya da
`KeyError` olursa `{"error": "wrong arguments"}`; çağrıda `arguments` yoksa
boş sözlük kullan.

**Beklenen çıktı:**

```
{'status': 'shipped'}
{'error': 'wrong arguments'}
{'error': 'wrong arguments'}
{'error': 'unknown tool refund'}
```
