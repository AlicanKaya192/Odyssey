Harvard'ın bulunduğu Massachusetts'te arabana harf ve rakamlarını kendin seçtiğin bir plaka isteyebilirsin. Şartlar:

- Plaka en az iki **harfle** başlamalı.
- En az 2, en çok 6 karakter (harf ya da rakam).
- Rakamlar ortada olamaz, sonda olmalı: `AAA222` olur, `AAA22A` olmaz. İlk rakam `0` olamaz.
- Nokta, boşluk ya da noktalama işareti olmaz.

Kullanıcıdan bir plaka isteyen ve şartların hepsine uyuyorsa `Valid`, uymuyorsa `Invalid` yazan bir program yaz. Harflerin büyük olacağını varsay. Programı başlangıç kodundaki düzene göre yaz: `is_valid(s)` şartlar sağlanıyorsa `True`, değilse `False` döndürsün. İstersen her şart için ayrı fonksiyon yazabilirsin. (CS50'de dosyanın adı `plates.py`.)

İpucu (CS50'den): dizelerin `isalpha` (hepsi harf mi), `isdigit` (hepsi rakam mı) ve `isalnum` (hepsi harf ya da rakam mı) metotları var; `s[0]` ilk harf.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `CS50` → çıktı `Valid`
- Girdi `CS05` → çıktı `Invalid`
- Girdi `CS50P` → çıktı `Invalid`
- Girdi `PI3.14` → çıktı `Invalid`
- Girdi `H` → çıktı `Invalid`
- Girdi `OUTATIME` → çıktı `Invalid`
- Girdi `AAA222` → çıktı `Valid`
- Girdi `AAA22A` → çıktı `Invalid`
- Girdi `50CS` → çıktı `Invalid`
- Girdi `NRVOUS` → çıktı `Valid`
