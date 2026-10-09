`timed(results, label)` bağlam yöneticisi blok süresini `results[label]`'a
yazıyor ama blokta hata çıkınca yazmıyor. Toparlamayı `try/finally` ile
düzelt: süre her durumda kaydedilsin.

**Beklenen çıktı:**

```
['failed', 'ok']
```
