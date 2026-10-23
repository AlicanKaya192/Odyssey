Problem Set 2'deki **Kişisel Plakalar**'ı yeniden yaz. Şartlar aynı:

- En az iki **harfle** başlar.
- En az 2, en çok 6 karakter.
- Rakamlar ortada olamaz, sonda olur (`AAA222` olur, `AAA22A` olmaz); ilk rakam `0` olamaz.
- Nokta, boşluk ya da noktalama işareti olmaz.

`is_valid(s)` şartların hepsi tutarsa `True`, değilse `False` döndürür; yalnızca `main` yazar. `main` dosya doğrudan çalışınca çağrılır (`if __name__ == "__main__":`). Harflerin büyük olacağını varsay.

Sonra `test_plates.py`'ye `is_valid`'i iyice sınayan, adı `test_` ile başlayan **dört ya da daha çok** fonksiyon yaz. Bozuk sürümlerin her biri şartlardan birini unutuyor; her şartı ayrı bir örnekle dene.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `CS50` → çıktı `Valid`
- Girdi `CS05` → çıktı `Invalid`
- Girdi `PI3.14` → çıktı `Invalid`
- Girdi `H` → çıktı `Invalid`
- Girdi `OUTATIME` → çıktı `Invalid`

Testlerin için: Odyssey `test_plates.py` dosyasını önce **senin** `plates.py` dosyanla çalıştırır (hepsi geçmeli), sonra `plates.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
