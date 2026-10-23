Başlangıç kodundaki `sheep(n)` bütün sürüyü bir listede kurup bir kerede döndürüyor; çok büyük `n`'de bellek yetmez. Onu bir **üretece** çevir: liste ve `append` olmadan, her satırı `yield` ile birer birer versin. `main` değişmiyor; çıktı aynı kalmalı (`1 sheep`, `2 sheep`, ...).

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
What's n? 3
1 sheep
2 sheep
3 sheep
```
