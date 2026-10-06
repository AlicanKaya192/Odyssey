Başlangıç kodundaki üç satırın üçü de çalışıyor ama **yanlış sonuç**
veriyor. Her satırın üstünde ne hesaplanmak istendiği yazıyor. Sayılara
dokunmadan, yalnızca **parantez ekleyerek** düzelt.

Düzelince çıktı şu olmalı:

```
80.0 4 8
```

Python işlemleri soldan sağa değil, bir öncelik sırasıyla yapar:

1. `**` (üs alma) en önce
2. Sonra işaret: `-2` gibi eksi
3. Sonra `*`, `/`, `//`, `%`
4. En son `+` ve `-` (bunlar kendi aralarında soldan sağa)

Parantez her şeyin önüne geçer.

> Dikkat: `-2 ** 2` sonucunun `4` değil `-4` çıkması çoğu kişiyi şaşırtır:
> Python önce `2 ** 2`'yi hesaplayıp sonra eksiyi uyguluyor.
