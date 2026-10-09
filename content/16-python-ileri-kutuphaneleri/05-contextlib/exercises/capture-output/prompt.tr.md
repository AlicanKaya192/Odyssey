`capture(func, *args)` fonksiyonunu yaz: `func(*args)`'ı çalıştırırken
yazdırdığı her şeyi `redirect_stdout` ile bir `io.StringIO`'ya yönlendirsin
ve yakalanan metni döndürsün.

**Beklenen çıktı:**

```
'hello ada\nbye\n'
```
