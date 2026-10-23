Bir **IPv4 adresi** noktayla ayrılmış dört sayıdır, `#.#.#.#`; her biri 0 ile 255 arasında (`255.255.255.255` geçerli, `512.512.512.512` değil). `numb3rs.py`'de `validate(ip)` yaz: bir metin alır, geçerli bir IPv4 adresiyse `True`, değilse `False` döndürür. `main` adresi sorar ve `validate`'in sonucunu (`True` ya da `False`) yazar. Sayıların aralığını kalıpla denetlemek zor; kalıpla biçimi denetle, aralığı `int` ile.

Sonra `test_numb3rs.py`'ye `validate`'i iyice sınayan, adı `test_` ile başlayan **iki ya da daha çok** fonksiyon yaz.

## Nasıl denenir

Programın için durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `127.0.0.1` → çıktı `True`
- Girdi `255.255.255.255` → çıktı `True`
- Girdi `512.512.512.512` → çıktı `False`
- Girdi `1.2.3.1000` → çıktı `False`
- Girdi `cat` → çıktı `False`

Testlerin için: Odyssey `test_numb3rs.py` dosyasını önce **senin** `numb3rs.py` dosyanla çalıştırır (hepsi geçmeli), sonra `numb3rs.py`'nin bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli). CS50'nin check50'si de testleri böyle sınıyor.
