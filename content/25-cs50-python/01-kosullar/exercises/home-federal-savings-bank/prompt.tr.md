*Seinfeld*'in bir bölümünde Kramer, "hello" diye selamlanmayan herkese 100 dolar vereceğini söyleyen bir bankaya gider. Ona "hey" denir; bunun "hello" olmadığını söyleyip 100 dolar ister. Müdür uzlaşma önerir: "'h' ile başlayan bir selam aldın, 20 dolara ne dersin?" Kramer kabul eder.

Kullanıcıdan bir selam isteyen bir program yaz. Selam `hello` ile başlıyorsa `$0`, `h` ile başlıyorsa (ama `hello` değilse) `$20`, başka bir şeyse `$100` yaz. Baştaki boşlukları yok say, büyük/küçük harfe bakma. `hello there`, `hello, Newman` gibi selamlar da `$0`. (CS50'de dosyanın adı `bank.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Hello` → çıktı `$0`
- Girdi `Hello, Newman` → çıktı `$0`
- Girdi `How you doing?` → çıktı `$20`
- Girdi `What's happening?` → çıktı `$100`
- Girdi `   hey` → çıktı `$20`
