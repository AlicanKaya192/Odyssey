`classify(text)` adres geri döngüyse `"loopback"`, özelse `"private"`,
değilse `"public"` döndürsün (`is_loopback`, `is_private`). Başlangıç kodu
çalışıyor ama `127.0.0.1` için yanlış cevap veriyor; nedenini bul.

**Beklenen çıktı:**

```
127.0.0.1 loopback
10.1.2.3 private
172.31.0.9 private
172.32.0.9 public
100.20.30.40 public
```
