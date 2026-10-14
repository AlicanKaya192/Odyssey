`ages.py` metni yaşa çeviriyor. Sayı değilse ya da 0–150 dışındaysa `ValueError` veriyor.

`main.py`'ye en az **dört** test yaz:

- `parse_age("42")` → `42`
- `parse_age("abc")` → `ValueError`
- `parse_age("-1")` → `ValueError`
- `parse_age("200")` → `ValueError`

Hata bekleyen testlerde `with pytest.raises(ValueError):` kullan.
