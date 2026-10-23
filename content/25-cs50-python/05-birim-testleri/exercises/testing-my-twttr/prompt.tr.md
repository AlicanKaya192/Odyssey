Problem Set 2'deki **Just setting up my twttr**'ı yeniden yaz: bu kez sesli harfleri (A, E, I, O, U; büyük ya da küçük) atan iş `shorten(word)` fonksiyonunda olsun. `shorten` bir metin alır ve sesli harfleri atılmış hâlini **döndürür** (`return`), yazmaz; yalnızca `main` `print` çağırır. Başlangıç kodundaki düzen CS50'nin istediği: `main`, `shorten` ve sonda `if __name__ == "__main__":`.

Sonra `test_twttr.py`'ye `shorten`'ı iyice sınayan, adı `test_` ile başlayan bir ya da daha çok fonksiyon yaz. `from twttr import shorten` hazır.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Twitter` → çıktı `Twttr`
- Girdi `What's your name?` → çıktı `Wht's yr nm?`
- Girdi `CS50` → çıktı `CS50`

Testlerin için: Odyssey `test_twttr.py` dosyasını önce **senin** `twttr.py` dosyanla çalıştırır (hepsi geçmeli), sonra `twttr.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
