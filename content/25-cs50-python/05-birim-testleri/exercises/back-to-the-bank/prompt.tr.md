Problem Set 1'deki **Home Federal Tasarruf Bankası**'nı yeniden yaz: tutarı bulan iş `value(greeting)` fonksiyonunda olsun. `value` bir metin alır ve bir **tam sayı** döndürür: selam `hello` ile başlıyorsa `0`, `h` ile başlıyorsa (ama `hello` değilse) `20`, başka bir şeyse `100`. Büyük/küçük harfe bakmaz; baştaki boşluk olmadığını varsayabilirsin (onu `main` siler). `main` tutarı `$20` biçiminde yazar.

Sonra `test_bank.py`'ye `value`'yu iyice sınayan, adı `test_` ile başlayan **üç ya da daha çok** fonksiyon yaz.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Hello` → çıktı `$0`
- Girdi `Hello, Newman` → çıktı `$0`
- Girdi `How you doing?` → çıktı `$20`
- Girdi `What's happening?` → çıktı `$100`
- Girdi `   hey` → çıktı `$20`

Testlerin için: Odyssey `test_bank.py` dosyasını önce **senin** `bank.py` dosyanla çalıştırır (hepsi geçmeli), sonra `bank.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
