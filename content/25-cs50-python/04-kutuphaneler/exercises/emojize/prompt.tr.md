Emoji dizüstü bilgisayarda kolay yazılmıyor; bu yüzden bazı programlar **kod** kabul ediyor: `:thumbs_up:` yazınca 👍 çıkıyor. Bazıları daha kısa **takma adları** da tanıyor: `:thumbsup:` da 👍.

Kullanıcıdan İngilizce bir metin isteyen ve içindeki kodları (ve takma adları) emojiye çevirip `Output: ...` biçiminde yazan bir program yaz. (CS50'de dosyanın adı `emojize.py`.)

İpucu (CS50'den): `emoji` paketinin `emojize` fonksiyonu bu işi yapar; takma adlar için `language="alias"` argümanı gerekir.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `:1st_place_medal:` → çıktı `Output: 🥇`
- Girdi `:money_bag:` → çıktı `Output: 💰`
- Girdi `:smile_cat:` → çıktı `Output: 😸`
- Girdi `hello, :earth_africa:` → çıktı `Output: hello, 🌍`
- Girdi `I :thumbsup: it` → çıktı `Output: I 👍 it`
