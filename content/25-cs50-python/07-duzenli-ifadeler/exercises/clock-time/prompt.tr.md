Kullanıcıdan 24 saatlik biçimde bir saat al (`09:30`) ve `re.fullmatch` ile doğrula: saat iki basamak, `00`–`23`; dakika iki basamak, `00`–`59`. Geçerliyse `Valid`, değilse `Invalid` yaz. `9:30` geçersiz (saat iki basamak olmalı).

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Time: 09:30
Valid
```
