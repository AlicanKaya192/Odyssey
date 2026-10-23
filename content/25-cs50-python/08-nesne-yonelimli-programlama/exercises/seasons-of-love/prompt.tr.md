Bir yıl, şarkıdaki gibi 525.600 dakika. Kullanıcıdan doğum tarihini `YYYY-MM-DD` biçiminde al (`1999-01-01`) ve doğduğu günden bugüne kaç dakika geçtiğini **yazıyla**, İngilizce yaz: `Five hundred twenty-five thousand, six hundred minutes`. Kişinin gece yarısı doğduğunu ve şu anın da bugünün gece yarısı olduğunu varsay; yani gün sayısı × 24 × 60. Sayıyı yazıya `inflect` çeviriyor (`p.number_to_words(n, andword="")`: CS50'nin istediği gibi arada `and` olmasın); sonuç büyük harfle başlar ve ` minutes` ile biter.

İş iki fonksiyonda olsun:

- `minutes_between(birth, today)`: iki tarih metni alır, aradaki dakikayı tam sayı olarak döndürür. Tarih geçersizse (`January 1, 1999`, `1999-02-30`) `ValueError` verir; `date.fromisoformat` bunu zaten yapıyor.
- `sing(minutes)`: dakikayı yazıya çevirip döndürür.

`main` doğum tarihini sorar, bugünü `date.today().isoformat()` ile verip sonucu yazar; tarih geçersizse `sys.exit("Invalid date")` ile çıkar, hata fırlatmaz. (`today`'i parametre yaptık ki testler her gün aynı sonucu versin.)

Sonra `test_seasons.py`'ye `main` dışındaki iki fonksiyonu iyice sınayan, adı `test_` ile başlayan fonksiyonlar yaz.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `January 1, 1999` → çıktı (boş) (çıkış kodu 1)
- Girdi `1999-02-30` → çıktı (boş) (çıkış kodu 1)
- Girdi `cat` → çıktı (boş) (çıkış kodu 1)

Testlerin için: Odyssey `test_seasons.py` dosyasını önce **senin** `seasons.py` dosyanla çalıştırır (hepsi geçmeli), sonra `seasons.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
