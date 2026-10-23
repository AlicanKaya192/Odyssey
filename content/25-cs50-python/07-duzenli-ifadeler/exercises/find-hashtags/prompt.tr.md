Kullanıcıdan bir gönderi al ve içindeki her etiketi (`#` ve ardından gelen kelime karakterleri) `re.findall` ile bul. Her birini `#`'sız ve küçük harfle ayrı satıra yaz. Etiket yoksa hiçbir şey yazma.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Post: Learning #Python with #CS50 today
python
cs50
```
