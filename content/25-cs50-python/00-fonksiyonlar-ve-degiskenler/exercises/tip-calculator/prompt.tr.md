ABD'de restoranda garsona bahşiş bırakmak gelenektir, genellikle hesabın %15'i ya da fazlası. Bahşiş hesaplayıcının çoğunu senin için yazdık (başlangıç kodu); ama iki fonksiyona vakit kalmadı:

- `dollars_to_float(d)`: `$##.##` biçiminde bir `str` alsın (her `#` bir rakam), baştaki `$`'ı atsın ve tutarı `float` döndürsün. `"$50.00"` için `50.0`.
- `percent_to_float(p)`: `##%` biçiminde bir `str` alsın, sondaki `%`'yi atsın ve yüzdeyi `float` döndürsün. `"15%"` için `0.15`.

Kullanıcının değerleri bu biçimde gireceğini varsayabilirsin. `main`'e dokunma. (CS50'de dosyanın adı `tip.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `$50.00`, `15%` → çıktı `Leave $7.50`
- Girdi `$100.00`, `18%` → çıktı `Leave $18.00`
- Girdi `$15.00`, `25%` → çıktı `Leave $3.75`
