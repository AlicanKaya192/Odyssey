`safe_top(argv)` fonksiyonunu yaz: `exit_on_error=False` ile bir
ayrıştırıcı kursun, `int` türünde `--top` (varsayılan 5) tanımlasın.
Ayrıştırma başarılıysa `top` değerini, `ArgumentError` gelirse `"invalid"`
metnini döndürsün; program çıkmasın.

**Beklenen çıktı:**

```
3 invalid 5
```
