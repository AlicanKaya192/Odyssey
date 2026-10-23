Bitcoin bir kripto para: bankaya değil, işlemleri kaydeden dağıtık bir ağa (blokzincir) dayanıyor.

Şu programı yaz:

- Kullanıcının almak istediği Bitcoin miktarını (`n`) **komut satırı argümanı** olarak bekler. Argüman yoksa `sys.exit("Missing command-line argument")`, `float`'a çevrilemiyorsa `sys.exit("Command-line argument is not a number")` ile çıkar.
- Bitcoin fiyatını API'den ister: `http://api.odyssey.test/v3/assets/bitcoin`. Cevap bir JSON nesnesi; fiyat `data` içindeki `priceUsd` anahtarında, metin olarak. `requests.RequestException`'ı yakala.
- `n` Bitcoin'in dolar cinsinden fiyatını **virgülden sonra dört basamakla** ve binlik ayırıcı olarak `,` ile yazar: `$97,534.2892`.

CS50'de istek CoinCap'in gerçek API'sine gidiyor ve bir API anahtarı istiyor. Burada Odyssey'nin kendi alıştırma sunucusu var: aynı biçimde cevap veriyor, internete çıkmıyor, fiyatı **sabit**. (CS50'de dosyanın adı `bitcoin.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi yok → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py cat` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py 1` → çıktı `$97,534.2892`
- Komut `python cozum.py 2` → çıktı `$195,068.5783`
- Komut `python cozum.py 2.5` → çıktı `$243,835.7229`
- Komut `python cozum.py 0.001` → çıktı `$97.5343`
