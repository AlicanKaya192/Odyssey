`version_ok(info, minimum)` fonksiyonunu yaz: `info` bir sürüm
(`(3, 14, 7)` ya da `sys.version_info`), `minimum` en düşük sürüm
(`(3, 10)`). `info`'nun ilk `len(minimum)` parçası `minimum`'a eşit ya da
büyükse `True` döndürsün. İkisini de `tuple(...)` yapıp karşılaştır.

**Beklenen çıktı:**

```
True
False
True
```
