Bir kurabiye kavanozunu sınıfla temsil et. `jar.py`'deki `Jar` sınıfının iskeleti CS50'nin verdiği gibi; parametreleri değiştirme, istersen kendi metotlarını ekle.

- `__init__(capacity=12)`: kavanozun alabileceği en fazla kurabiye. `capacity` negatif olmayan bir `int` değilse `ValueError`. Kavanoz boş başlar.
- `__str__`: kavanozdaki her kurabiye için bir `🍪`; 3 kurabiyede `🍪🍪🍪`. Emoji klavyende yok; başlangıç kodundaki `COOKIE` sabitini kullan (`COOKIE * 3`).
- `deposit(n)`: `n` kurabiye ekler; kapasite aşılacaksa `ValueError`.
- `withdraw(n)`: `n` kurabiye alır; kavanozda `n`'den az varsa `ValueError`.
- `capacity` (özellik): kapasite.
- `size` (özellik): kavanozdaki kurabiye sayısı.

Sonra `test_jar.py`'ye `Jar`'ı iyice sınayan, adı `test_` ile başlayan **dört ya da daha çok** fonksiyon yaz (`test_init`, `test_str`, `test_deposit`, `test_withdraw` gibi). Kurabiyeleri karşılaştırırken de `COOKIE` kullan: `assert str(jar) == COOKIE * 3`.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.



Testlerin için: Odyssey `test_jar.py` dosyasını önce **senin** `jar.py` dosyanla çalıştırır (hepsi geçmeli), sonra `jar.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
