`working.py`'de `convert(s)` yaz: 12 saatlik biçimde iki saat alır, `9:00 AM to 5:00 PM` ya da kısaca `9 AM to 5 PM`, ve 24 saatlik biçimde döndürür: `09:00 to 17:00`. İki saat farklı biçimde olabilir (`9 AM to 5:30 PM`). `AM` ve `PM` büyük harf, önlerinde bir boşluk var. Mesainin sabah başladığını varsayma: `10 PM to 8 AM` → `22:00 to 08:00`. `12 AM` gece yarısı (`00:00`), `12 PM` öğle (`12:00`). Saatlerden biri geçersizse (`9:60 AM`, `13 PM`) ya da girdi bu biçimde değilse (`9 AM - 5 PM`) `ValueError` ver; yakalama, program çöksün. `main` saatleri sorar ve `convert`'in sonucunu yazar.

Sonra `test_working.py`'ye `convert`'i iyice sınayan, adı `test_` ile başlayan **üç ya da daha çok** fonksiyon yaz.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `9 AM to 5 PM` → çıktı `09:00 to 17:00`
- Girdi `9:00 AM to 5:00 PM` → çıktı `09:00 to 17:00`
- Girdi `10 PM to 8 AM` → çıktı `22:00 to 08:00`
- Girdi `10:30 PM to 8:50 AM` → çıktı `22:30 to 08:50`

Testlerin için: Odyssey `test_working.py` dosyasını önce **senin** `working.py` dosyanla çalıştırır (hepsi geçmeli), sonra `working.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
