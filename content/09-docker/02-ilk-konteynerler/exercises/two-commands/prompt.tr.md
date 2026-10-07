Bir konteynerin tek bir asıl programı var. Birden çok komutu art arda
çalıştırmak için onları bir kabuğa veriyorsun: `sh -c "komut1 && komut2"`.
`&&` "öncekisi başarılıysa sonrakini çalıştır" demek.

**Yapman gereken:** `CMD` satırını yaz: `sh -c` ile önce `echo start`, sonra
`echo done` çalışsın. Köşeli parantezli biçimde üç parça var: `"sh"`, `"-c"`
ve tırnak içindeki satırın tamamı.

Bu alıştırma imajı gerçekten kurup çalıştırıyor (Docker açık olmalı).

**Beklenen çıktı:**

```
start
done
```
