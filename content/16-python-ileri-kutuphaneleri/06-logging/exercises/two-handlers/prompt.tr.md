`setup()` fonksiyonunu yaz: `"app"` kaydedicisinin düzeyi `DEBUG`; iki
işleyici eklesin: ekrana (`sys.stdout`) yalnızca `WARNING` ve üstü,
`"%(levelname)s: %(message)s"` biçiminde; `app.log` dosyasına (`utf-8`) her
şey, `"%(levelname)s %(message)s"` biçiminde.

**Beklenen çıktı:**

```
WARNING: config missing
DEBUG reading config
WARNING config missing
```
