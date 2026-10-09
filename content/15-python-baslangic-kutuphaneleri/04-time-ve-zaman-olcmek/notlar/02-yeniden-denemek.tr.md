İnternetten veri çeken, bir veritabanına bağlanan ya da başka bir programı
bekleyen kod bazen geçici bir hatayla karşılaşır: sunucu o an meşguldür, ağ
bir anlığına kopmuştur. Böyle hatalarda hemen vazgeçmek yerine **biraz
bekleyip yeniden denemek** yaygın bir kalıptır.

## Üstel bekleme (exponential backoff)

Her başarısız denemeden sonra bekleme süresi **ikiye katlanır**: 1, 2, 4, 8...
Sunucu gerçekten zorlanıyorsa herkesin aynı anda yeniden saldırması onu daha
da zorlar; giderek uzayan beklemeler ona nefes aldırır.

```python
import time


def retry(func, attempts=5, base=0.01):
    waits = []
    for attempt in range(attempts):
        try:
            return func(), waits
        except ConnectionError:
            if attempt == attempts - 1:
                raise
            wait = base * 2 ** attempt
            waits.append(wait)
            time.sleep(wait)


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 4:
        raise ConnectionError("server busy")
    return "ok"


print(retry(flaky))
print(calls["n"])
```

```text
('ok', [0.01, 0.02, 0.04])
4
```

`flaky` ilk üç çağrıda hata veriyor, dördüncüde çalışıyor. `retry` her
hatadan sonra 0,01, 0,02, 0,04 saniye bekledi ve dördüncü denemede sonucu
döndürdü. Son deneme de düşerse `raise` hatayı yukarı iletir: sonsuza kadar
denemek de bir hatadır.

Örnekte süreleri kısa tuttuk; gerçek programlarda taban genelde 0,5–1
saniyedir ve bekleme bir üst sınırla kesilir (`min(üst_sınır, ...)`): taban 1
saniyeyse onuncu denemeden önce 2⁸ = 256 saniye, yani 4 dakikadan fazla
beklenirdi.

## Neyi yeniden denemeli?

- **Geçici** hatalar: bağlantı koptu, zaman aşımı, "sunucu meşgul" (HTTP
  `503`, `429`).
- **Kalıcı** hatalar yeniden denenmez: yanlış adres (`404`), yetki yok
  (`401`), kodundaki bir `TypeError`. Kaç kez denersen dene sonuç aynı.

`except` satırında yalnızca geçici hataları yakala (`ConnectionError`,
`TimeoutError`); çıplak `except:` her hatayı yeniden dener ve gerçek hatayı
gizler.
