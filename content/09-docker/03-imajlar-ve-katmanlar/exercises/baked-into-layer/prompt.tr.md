Bir önceki bölümde konteynerin içine yazılan dosya konteyner silinince
kayboluyordu. **Derleme sırasında** yazılan dosya ise imajın katmanına
giriyor ve imajdan çalıştırılan **her** konteynerde bulunuyor.

`RUN` talimatı derleme sırasında bir komut çalıştırıyor ve sonucunu yeni bir
katman olarak kaydediyor.

**Yapman gerekenler:**

1. `RUN` ile `/built.txt` dosyasına `made at build time` yazdır.
2. `CMD` ile konteyner çalışınca `cat /built.txt` çalışsın.

**Beklenen çıktı:**

```
made at build time
```
