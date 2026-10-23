FIGlet (adını Frank, Ian ve Glen'in harflerinden alıyor) 1990'ların başından kalma, sıradan metinden büyük harfler çizen bir program: bir tür ASCII sanatı. Python'a `pyfiglet` paketi olarak taşındı.

Şu programı yaz:

- **Sıfır ya da iki** komut satırı argümanı bekler. Sıfırsa metni rastgele bir yazı tipiyle yazar. İkiyse birincisi `-f` ya da `--font`, ikincisi yazı tipinin adı olmalı.
- Kullanıcıdan bir metin ister.
- Metni istenen yazı tipiyle yazar: önce `Output:`, alt satırdan itibaren çizim.

Argümanlar bu kurala uymuyorsa (birincisi `-f` / `--font` değil, ikincisi bir yazı tipi adı değil, sayıları yanlış) program `sys.exit("Invalid usage")` ile çıksın. (CS50'de dosyanın adı `figlet.py`.)

İpucu (CS50'den): `from pyfiglet import Figlet`, `figlet = Figlet()`; `figlet.getFonts()` yazı tiplerinin listesini verir, `figlet.setFont(font=f)` yazı tipini seçer, `figlet.renderText(s)` çizimi metin olarak döndürür. Rastgele seçim için `random.choice`.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Komut `python cozum.py test` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py -a slant` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py -f invalid_font` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py -f slant`, girdi `CS50` → çıktı:

```text
Output:
   ___________ __________ 
  / ____/ ___// ____/ __ \
 / /    \__ \/___ \/ / / /
/ /___ ___/ /___/ / /_/ / 
\____//____/_____/\____/  
                          
```

- Komut `python cozum.py -f rectangles`, girdi `Hello` → çıktı:

```text
Output:
                   
 _____     _ _     
|  |  |___| | |___ 
|     | -_| | | . |
|__|__|___|_|_|___|
                   
```

- Komut `python cozum.py --font alphabet`, girdi `Moo` → çıktı:

```text
Output:
M   M         
MM MM         
M M M ooo ooo 
M   M o o o o 
M   M ooo ooo 
              
              
```

- Girdi `hi` → çıktı:

```text
Output:
.%%..%%..%%%%%%.
.%%..%%....%%...
.%%%%%%....%%...
.%%..%%....%%...
.%%..%%..%%%%%%.
................
```

