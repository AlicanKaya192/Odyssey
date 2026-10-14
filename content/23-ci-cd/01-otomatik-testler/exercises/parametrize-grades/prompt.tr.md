`grades.py` bir puanı harf notuna çeviriyor: 90 ve üstü `A`, 80 ve üstü `B`, 70 ve üstü `C`, altı `F`.

`main.py`'ye `@pytest.mark.parametrize` kullanan **tek** bir test yaz. En az **beş** satırı olsun ve sınırları denesin:

- `90` → `A`, `89` → `B`
- `80` → `B`, `79` → `C`
- `70` → `C`, `69` → `F`

Her satır ayrı bir test sayılır.
