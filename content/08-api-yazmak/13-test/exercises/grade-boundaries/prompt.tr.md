`GET /grade?score=...` puanı harfe çeviriyor: 90 ve üstü `A`, 80 ve üstü
`B`, 70 ve üstü `C`, altı `F`; 0–100 dışı `422`.

**Yapman gereken:** `@pytest.mark.parametrize` ile sınırları deneyen
testler yaz (en az 5 test). Bozuk sürümlerde `>=` yerine `>` yazılmış ya da
üst sınır kaldırılmış olacak; testlerin bunları yakalamalı.
