Emoji'den önce ifadeler (emoticon) vardı: `:)` mutlu, `:(` üzgün yüzdü.

`convert` adında bir fonksiyon yaz: bir `str` alsın ve aynı metni her `:)` yerine `[happy]`, her `:(` yerine `[sad]` koyarak **döndürsün**; geri kalan metin değişmesin. Aynı dosyada bir `main` fonksiyonu yaz: kullanıcıdan girdi istesin, `convert`'i çağırsın ve sonucu yazsın. Dosyanın sonunda `main`'i çağırmayı unutma.

*CS50'de yüzler emoji'ye (🙂 🙁) çevriliyor; Odyssey'de yazdığın kod ve çıktı klavyede olan karakterlerle yazılsın diye `[happy]` / `[sad]` kullanıyoruz.* (CS50'de dosyanın adı `faces.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Hello :)` → çıktı `Hello [happy]`
- Girdi `Goodbye :(` → çıktı `Goodbye [sad]`
- Girdi `Hello :) Goodbye :(` → çıktı `Hello [happy] Goodbye [sad]`
