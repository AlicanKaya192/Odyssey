Bu Dockerfile programı `RUN` ile çalıştırıyor. İmaj kurulurken program bir
kez çalışıp bitiyor; konteyner açılınca ise hiçbir şey olmuyor (bu imajın
varsayılan komutu etkileşimli Python ve hemen kapanıyor).

**Yapman gereken:** son satırı, programı **konteyner çalışınca** çalıştıracak
şekilde değiştir (köşeli parantezli biçim).

**Beklenen çıktı** (konteynerin yazdığı):

```
the clock is ticking
```
