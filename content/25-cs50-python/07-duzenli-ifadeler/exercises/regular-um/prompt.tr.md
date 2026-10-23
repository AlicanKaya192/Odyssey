Konuşurken araya giren "um"ları saymak istiyoruz. `um.py`'de `count(s)` yaz: bir metin alır ve içinde `um`'un **ayrı bir kelime** olarak kaç kez geçtiğini tam sayı olarak döndürür; büyük/küçük harf fark etmez. Başka bir kelimenin içindeki `um` sayılmaz: `yummy`'de, `album`'de, `umbrella`'da yok. `main` metni sorar ve sonucu yazar.

Sonra `test_um.py`'ye `count`'u iyice sınayan, adı `test_` ile başlayan **üç ya da daha çok** fonksiyon yaz.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `hello, um, world` → çıktı `1`
- Girdi `Um, thanks for the album.` → çıktı `1`
- Girdi `Um, thanks, um...` → çıktı `2`
- Girdi `yummy` → çıktı `0`

Testlerin için: Odyssey `test_um.py` dosyasını önce **senin** `um.py` dosyanla çalıştırır (hepsi geçmeli), sonra `um.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
