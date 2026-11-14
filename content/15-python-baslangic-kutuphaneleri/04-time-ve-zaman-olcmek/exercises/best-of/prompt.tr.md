`measure(func, repeat)` fonksiyonunu yaz: `func`'ı `repeat` kez çağırsın,
her çağrının süresini `time.perf_counter()` ile ölçsün ve **en kısa** süreyi
saniye olarak döndürsün. Alttaki satırlar fonksiyonu sınıyor: çağrı sayısını
sayıyor ve süreleri 0,6, 0,05, 0,4 saniye olan üç çağrıda en kısasını
bekliyor.

**Beklenen çıktı:**

```
True
4
True
True
```
