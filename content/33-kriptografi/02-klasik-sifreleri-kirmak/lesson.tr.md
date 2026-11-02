# Klasik Şifreleri Kırmak

Klasik Şifreler bölümünde her şifrenin bir zayıflığı olduğunu söyledik.
Bu bölümde hepsini gerçekten kırıyoruz. Amaç saldırı öğrenmek değil,
**bir şifrenin neden yetmediğini ölçerek görmek**: anahtarı bilmeyen biri
şifreli metinden düz metne ne kadar kolay ulaşıyor? Bu soruya verilen
cevaplar, modern şifrelerin nasıl tasarlandığını belirledi.

Saldırgan için iki durumu ayırırız:

- **Yalnızca şifreli metin** (ciphertext-only): elinde sadece şifreli
  metin var. Bu bölümdeki bütün saldırılar böyle.
- **Bilinen düz metin** (known-plaintext): bazı düz metin–şifreli metin
  çiftlerini biliyor. XOR ve Tek Kullanımlık Şifre bölümünde göreceğiz.

Örneklerde kullandığımız metin `cipher_data.py` dosyasında: 704 harflik
İngilizce bir paragraf (`SAMPLE`) ve İngilizcede harflerin yaklaşık
yüzdeleri (`ENGLISH_FREQ`).

## Sezar: bütün anahtarları dene

26 anahtar varsa hepsini denemek en kolay yoldur. Ama hangisinin doğru
olduğunu nasıl anlarız? Bilgisayar "anlamlı metin"i görmez; bir **ölçüt**
gerekir. En basiti: çözülen metinde sık kullanılan kelimeleri saymak.

```python
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


COMMON = {"the", "is", "and", "of", "in", "to"}
secret = "wkh vhfuhw lv lq wkh jdughq"
scores = []
for shift in range(26):
    words = caesar(secret, -shift).split()
    hits = sum(word in COMMON for word in words)
    scores.append((hits, shift))
best = max(scores)
print(len(scores), "keys tried")
print("best shift:", best[1], "->", caesar(secret, -best[1]))
```

```text
26 keys tried
best shift: 3 -> the secret is in the garden
```

26 deneme anlık sürdü ve doğru anahtar sık kelimelerle kendini belli etti.
Anahtar uzayı küçük olan her şifre böyle düşer.

## Harf sıklığı

Her dilde harfler eşit sıklıkta kullanılmaz. İngilizcede `e` en sık
harftir, ardından `t`, `a`, `o` gelir. Örnek metnimizde sayalım:

```python
from collections import Counter

from cipher_data import SAMPLE

letters = [ch for ch in SAMPLE.lower() if ch.isalpha()]
counts = Counter(letters)
for letter, n in counts.most_common(5):
    print(letter, f"{100 * n / len(letters):.1f}%")
```

```text
e 12.6%
t 10.7%
h 8.8%
a 8.5%
o 6.8%
```

Bu dağılım bir **parmak izi**dir. Sezar ya da yerine koyma şifresi harfleri
değiştirir ama dağılımı değiştirmez: düz metindeki `e` hangi harfe
dönüştüyse, şifreli metinde o harf en sık harf olur.

## Ki-kare ile en iyi kaydırma

Kelime listesi yerine bütün harfleri kullanan daha sağlam bir ölçüt
**ki-kare** (chi-squared) uzaklığıdır: her harf için beklenen sayıyla
görülen sayı arasındaki farkın karesi, beklenen sayıya bölünüp toplanır.
Metin İngilizceye ne kadar benziyorsa sonuç o kadar **küçük** çıkar.
Örnek metni bilmediğimiz bir kaydırmayla şifreleyip her kaydırmayı
puanlayalım:

```python
from cipher_data import SAMPLE, ENGLISH_FREQ


def chi_squared(text):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    total = len(letters)
    score = 0
    for letter, percent in ENGLISH_FREQ.items():
        expected = total * percent / 100
        observed = letters.count(letter)
        score += (observed - expected) ** 2 / expected
    return score


secret = caesar(SAMPLE, 7)
ranked = sorted((chi_squared(caesar(secret, -s)), s) for s in range(26))
for score, shift in ranked[:3]:
    print(f"shift {shift:>2}: {score:8.1f}")
```

```text
shift  7:     41.3
shift 13:   2620.1
shift 18:   3026.5
```

Doğru kaydırma (7) ikinci en iyiden altmış kattan fazla küçük bir puan
aldı. Hiçbir kelime listesi gerekmedi; yalnızca dilin istatistiği yetti.

## Yerine koyma şifresine ilk adım

Yerine koyma şifresinin 26! anahtarı var, kaba kuvvet işe yaramaz. Ama
harf sıklığı burada da çalışır: şifreli metindeki harfleri sıklığa göre
dizip İngilizcenin sırasıyla (`etaoinshr…`) eşleyelim.

```python
import string
from collections import Counter

from cipher_data import SAMPLE

key = "qwertyuiopasdfghjklzxcvbnm"
table = str.maketrans(string.ascii_lowercase, key)
secret = SAMPLE.lower().translate(table)

order = [ch for ch, _ in Counter(c for c in secret if c.isalpha()).most_common()]
guess = dict(zip(order, "etaoinshrdlcumwfgypbvkjxqz"))
real = dict(zip(key, string.ascii_lowercase))
right = sum(guess[ch] == real[ch] for ch in order)
print("letters in text:", len(order))
print("right at first try:", right)
print("most common:", order[0], "->", guess[order[0]])
```

```text
letters in text: 22
right at first try: 5
most common: t -> e
```

İlk denemede yalnızca birkaç harf doğru çıktı: 704 harflik bir metinde
sıklıklar İngilizcenin ortalamasına tam uymaz. Ama en sık harf `e`'ye
doğru eşlendi ve bu bir başlangıçtır. Gerçek çözümde buradan ilerlenir:
üç harfli en sık kelime büyük ihtimalle `the`, tek harfli kelimeler `a` ya
da `i`, çift harfler (`ll`, `ee`, `ss`)… Her doğru tahmin bir sonrakini
kolaylaştırır. Bu iş elle birkaç dakika, bir programla bir saniye sürer.

## Vigenère: anahtarın uzunluğunu bul

Vigenère aynı harfi farklı yerlerde farklı harflere çevirdiği için şifreli
metindeki harf dağılımı **düzleşir**. Bunu ölçen sayı **tesadüf indeksi**
(index of coincidence, IoC): metinden rastgele seçilen iki harfin aynı
çıkma olasılığı. İngilizce metinde yaklaşık 0,066, harflerin eşit dağıldığı
rastgele metinde 1/26 ≈ 0,038.

Anahtar uzunluğunu `L` tahmin edip metni `L` sütuna bölersek (her sütun
aynı anahtar harfiyle kaydırılmış harfler), doğru `L` için her sütun basit
bir Sezar şifresidir ve IoC İngilizcenin değerine çıkar:

```python
from collections import Counter

from cipher_data import SAMPLE


def vigenere(text, key):
    result, i = "", 0
    for ch in text.lower():
        if ch.isalpha():
            result += chr((ord(ch) - 97 + ord(key[i % len(key)]) - 97) % 26 + 97)
            i += 1
    return result


def ioc(letters):
    n = len(letters)
    return sum(v * (v - 1) for v in Counter(letters).values()) / (n * (n - 1))


secret = vigenere(SAMPLE, "lemon")
print("plain IoC: ", round(ioc([c for c in SAMPLE.lower() if c.isalpha()]), 4))
print("cipher IoC:", round(ioc(secret), 4))
for length in range(1, 8):
    columns = [secret[i::length] for i in range(length)]
    average = sum(ioc(col) for col in columns) / length
    print(length, round(average, 4))
```

```text
plain IoC:  0.0682
cipher IoC: 0.0416
1 0.0416
2 0.0412
3 0.0414
4 0.0414
5 0.0684
6 0.0404
7 0.0408
```

Şifreli metnin IoC'si 0,042'ye düştü: dağılım düzleşti. Ama uzunluk 5'te
sütunların ortalaması birden 0,068'e çıktı; anahtar `lemon` beş harfli.
Uzunluk bulununca her sütun ayrı bir Sezar şifresi olarak ki-kare ile
çözülür ve anahtarın harfleri tek tek ortaya çıkar. Charles Babbage ve
Friedrich Kasiski 19. yüzyılda bunu (farklı bir yöntemle) elle yaptı.

## Bu bölümden çıkan ders

| Şifre | Kırılma yolu | Ne gerekti? |
|---|---|---|
| Sezar | Kaba kuvvet | 26 deneme |
| Yerine koyma | Harf sıklığı + kelime kalıpları | Birkaç yüz harf |
| Vigenère | IoC ile uzunluk, sonra sütun sütun ki-kare | Birkaç yüz harf |
| Çit şifresi | Satır sayılarını denemek | Birkaç deneme |

Hepsinde ortak olan şu: şifreli metin, düz metnin **istatistiğini**
taşıyor. Modern bir şifreden beklenen, şifreli metnin anahtarı bilmeyen
biri için **rastgeleden ayırt edilemez** olmasıdır. Bunu ilk kez
mükemmel biçimde sağlayan yöntemi, tek kullanımlık şifreyi, sıradaki
bölümde göreceğiz.

## Özet

- **Kaba kuvvet** küçük anahtar uzayında yeter; doğru anahtarı tanımak için
  bir ölçüt gerekir (sık kelimeler, ki-kare).
- **Harf sıklığı** dilin parmak izidir; Sezar ve yerine koyma onu
  değiştirmez.
- **Ki-kare** düşük olan kaydırma doğru kaydırmadır.
- **Tesadüf indeksi** Vigenère'nin anahtar uzunluğunu verir; sonra her
  sütun ayrı bir Sezar'dır.
- Modern şifrenin hedefi: şifreli metin rastgeleden ayırt edilemesin.
