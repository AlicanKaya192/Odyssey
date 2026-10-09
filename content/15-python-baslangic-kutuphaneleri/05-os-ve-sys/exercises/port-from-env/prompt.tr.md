`port_from_env(default=8000)` fonksiyonunu yaz: `APP_PORT` ortam
değişkenini okusun ve **tam sayı** olarak döndürsün. Değişken yoksa ya da
yalnızca rakamlardan oluşmuyorsa (`str.isdigit`) `default` dönsün. Başlangıç
kodu değişken yokken çöküyor.

**Beklenen çıktı:**

```
8000
9090 int
8000
```
