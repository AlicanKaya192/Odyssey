Dışarıdan gelen bir paketin kaynağı iç ağdaysa ya da geri döngü
adresiyse paket sahtedir. `ingress_ok(src, internal)` bu durumda `False`,
değilse `True` döndürsün. `internal` iç ağın CIDR yazımı
(`"192.168.1.0/24"`). Başlangıç kodu geri döngüyü unutuyor.

**Beklenen çıktı:**

```
203.0.113.7 True
192.168.1.20 False
127.0.0.1 False
```
