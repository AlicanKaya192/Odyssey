Problem Set 3'teki **Yakıt Göstergesi**'ni üç fonksiyona bölerek yeniden yaz:

- `convert(fraction)`: `X/Y` biçiminde bir metin alır (`X` negatif olmayan, `Y` pozitif tam sayı) ve kesri en yakın tam sayıya yuvarlanmış yüzde olarak **döndürür** (0 ile 100 arası). `X` ya da `Y` tam sayı değilse ya da `X` `Y`'den büyükse `ValueError`, `Y` 0 ise `ZeroDivisionError` verir (`raise ValueError`).
- `gauge(percentage)`: bir tam sayı alır; 1 ya da daha azsa `"E"`, 99 ya da daha çoksa `"F"`, değilse sayının arkasına `%` koyup (`"75%"`) metin olarak döndürür.
- `main`: geçerli bir kesir gelene kadar sorar ve `gauge`'un sonucunu yazar. Yalnızca `main` `print` çağırır.

Sonra `test_fuel.py`'ye `convert`'i ve `gauge`'u iyice sınayan, adı `test_` ile başlayan **iki ya da daha çok** fonksiyon yaz. Hata beklenen durumlar için `pytest.raises`.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `3/4` → çıktı `75%`
- Girdi `1/100` → çıktı `E`
- Girdi `99/100` → çıktı `F`
- Girdi `cat`, `5/4`, `1/0`, `1/2` → çıktı `50%`

Testlerin için: Odyssey `test_fuel.py` dosyasını önce **senin** `fuel.py` dosyanla çalıştırır (hepsi geçmeli), sonra `fuel.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
