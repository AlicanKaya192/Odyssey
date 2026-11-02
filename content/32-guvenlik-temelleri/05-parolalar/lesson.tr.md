# Parolalar

Parola (password) en eski ve hâlâ en yaygın kimlik doğrulama yöntemidir.
Ucuzdur, her yerde çalışır, özel bir cihaz istemez. Zayıf yanı insanlardır:
akılda kalan parolalar tahmin edilir, tahmin edilemeyenler unutulur. Bu
bölüm bir parolanın ne kadar güçlü olduğunu nasıl ölçeceğini, nasıl
kırıldığını ve iyi bir parola kuralının neye benzediğini anlatıyor.

## Parolalar nasıl ele geçirilir?

- **Çevrimiçi tahmin** (online guessing): giriş sayfasında tek tek
  denemek. Her deneme sunucuya gider; deneme sınırı ve kilit bunu çok
  yavaşlatır.
- **Çevrimdışı tahmin** (offline guessing): saldırgan bir sızıntıda
  parolaların **özetlerini** ele geçirmiştir ve kendi bilgisayarında
  saniyede milyarlarca deneme yapar. Hiçbir deneme sınırı yoktur. Parola
  saklamanın neden bu kadar önemli olduğunu bir sonraki bölümde (Parolaları
  Saklamak) göreceğiz.
- **Sözlük saldırısı** (dictionary attack): her olasılığı değil, önce
  gerçek insanların seçtiği parolaları denemek. Sızıntılardan derlenmiş
  listeler milyonlarca gerçek parola içerir. Bunlara kurallar eklenir:
  büyük harfle başlat, sona yıl ekle, `a` yerine `@` yaz.
- **Kimlik bilgisi doldurma** (credential stuffing): bir sitede sızan
  kullanıcı adı ve parola çiftlerini başka sitelerde denemek. Aynı parolayı
  birden fazla yerde kullanan herkes bu yüzden risk altındadır.
- **Oltalama ve gözetleme:** parolayı sorarak ya da omuz üstünden bakarak
  almak (Sosyal Mühendislik bölümü).

## Parolanın gücü: entropi

Bir parolanın gücünü "kaç olasılık içinden seçildi" sorusu belirler. Bu
sayı büyük olduğu için **bit** cinsinden söylenir: `n` bitlik bir parola
`2^n` olasılıktan biridir. Buna **entropi** (entropy) denir.

Parola **rastgele** seçildiyse hesap kolaydır: alfabedeki karakter sayısı
`a`, uzunluk `n` ise olasılık sayısı `a^n`, entropi `n × log2(a)` bittir.

```python
import math

alphabets = [("digits", 10), ("lower", 26), ("letters+digits", 62), ("printable", 94)]
for name, size in alphabets:
    bits = [round(n * math.log2(size)) for n in (8, 12, 16)]
    print(f"{name:<15} {size:>3}  8:{bits[0]:>3} 12:{bits[1]:>3} 16:{bits[2]:>3}")
```

```text
digits           10  8: 27 12: 40 16: 53
lower            26  8: 38 12: 56 16: 75
letters+digits   62  8: 48 12: 71 16: 95
printable        94  8: 52 12: 79 16:105
```

Tabloyu yatay oku: aynı alfabede her karakter aynı miktarda bit ekliyor.
Dikey oku: alfabeyi büyütmek de bit ekliyor, ama daha az. 16 küçük harf
(75 bit) 12 karakterlik her türden karaktere (79 bit) neredeyse yetişiyor.
**Uzunluk, karmaşıklıktan daha çok kazandırır.**

## Kaç yıl sürer?

Rastgele bir parolayı bulmak için ortalama olarak olasılıkların yarısını
denemek gerekir: `2^(n-1)` deneme. Ne kadar süreceği saldırganın hızına
bağlı. Aşağıdaki iki hız **örnek**: deneme sınırlı bir giriş sayfası için
saniyede 10, hızlı bir özet fonksiyonuyla saklanmış parolalara çevrimdışı
saldırı için saniyede on milyar. Gerçek hız donanıma ve parolanın nasıl
saklandığına bağlıdır.

```python
def years(bits, guesses_per_second):
    seconds = 2 ** (bits - 1) / guesses_per_second
    return seconds / (365 * 24 * 3600)


for bits in [40, 60, 80]:
    print(bits, f"online {years(bits, 10):.1e}", f"offline {years(bits, 1e10):.1e}")
```

```text
40 online 1.7e+03 offline 1.7e-06
60 online 1.8e+09 offline 1.8e+00
80 online 1.9e+15 offline 1.9e+06
```

`1.7e+03` "1,7 × 10³" demek, yani yaklaşık 1700 yıl. 40 bitlik bir parola
çevrimiçi saldırıya bin yıldan fazla dayanıyor ama çevrimdışı saldırıda
bir dakika bile sürmüyor. 80 bit ise iki durumda da yeterli. Aradaki fark,
parolanın nasıl saklandığıyla ve deneme sınırıyla ilgili; ikisi de
savunanın elinde.

## İnsanların seçtiği parolalar

Entropi formülü yalnızca **rastgele** parolalar için doğrudur. İnsanlar
rastgele seçmez. `Summer2024!` on bir karakter; büyük harf, küçük harf,
rakam ve işaret içeriyor; formüle göre 72 bit. Ama "mevsim + yıl + ünlem"
kalıbı sözlük saldırılarının ilk denediği şeylerdendir; gerçek gücü
formülün söylediğinin çok altındadır.

Bu yüzden parola kuralları bilinen ve sızmış parolaları denetler:

```python
common = {"123456", "password", "qwerty", "summer2024!", "iloveyou"}
for pw in ["Summer2024!", "lamp-river-cloud-tiger", "Qwerty"]:
    print(f"{pw:<23}", "common" if pw.lower() in common else "not in list")
```

```text
Summer2024!             common
lamp-river-cloud-tiger  not in list
Qwerty                  common
```

Gerçek sistemler bu listeyi beş tane değil, sızıntılardan derlenmiş
milyonlarca parolayla tutar.

## Parola cümleleri

Uzun ve akılda kalan bir parola için iyi bir yol, **rastgele seçilmiş**
birkaç kelimeyi yan yana koymaktır: **parola cümlesi** (passphrase).
7776 kelimelik bir listeden (beş zarla seçilecek kadar) rastgele seçilen
her kelime şu kadar bit ekler:

```python
import math

per_word = math.log2(7776)
print(round(per_word, 2))
for words in [4, 5, 6]:
    print(words, "words:", round(words * per_word), "bits")
```

```text
12.92
4 words: 52 bits
5 words: 65 bits
6 words: 78 bits
```

Altı kelime yaklaşık 78 bit: tamamen rastgele seçilmiş 13
karakterlik bir harf-rakam parolası kadar (77 bit), ama
akılda kalması çok daha kolay. Şart, kelimeleri senin
değil **rastgeleliğin** seçmesidir; "anneminadı-doğumyılım" bir parola
cümlesi değildir.

## Parolayı bilgisayara ürettirmek

Python'da rastgele parola üretmek için `random` değil **`secrets`**
modülü kullanılır. `random` modülünün ürettiği sayılar tahmin edilebilir;
oyun ve benzetim için yazılmıştır. `secrets` ise işletim sisteminin güvenli
rastgelelik kaynağını kullanır (ayrıntısı Kriptografi modülünün Rastgelelik
bölümünde).

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password), all(c in alphabet for c in password))
```

```text
16 True
```

Üretilen parolayı buraya yazmadık: her çalıştırmada farklı. Bu kodun
çıktısı yalnızca uzunluğun 16 olduğunu ve her karakterin alfabeden geldiğini
gösteriyor.

## İyi bir parola kuralı

Uzun yıllar parola kuralları karmaşıklığı zorladı: "en az bir büyük harf,
bir rakam, bir işaret; her 90 günde değiştir". Ölçümler bunun ters
tepdiğini gösterdi: insanlar `Parola1!`, sonra `Parola2!` yazdı. Bugünkü
kılavuzlar şunu söylüyor:

| Yap | Yapma |
|---|---|
| Uzunluğu esas al (en az 8, tercihen 12+ karakter) | Zorunlu karakter türü kuralları koyma |
| Uzun parolalara ve boşluğa izin ver (en az 64 karakter) | Parolayı kısa bir sınırda kes |
| Bilinen ve sızmış parolaları reddet | Belirli aralıklarla değiştirmeyi zorlama |
| Yalnızca sızdığından şüphelenince değiştirt | İpucu ya da güvenlik sorusu kullanma |
| Yapıştırmaya ve parola yöneticisine izin ver | Yapıştırmayı engelleme |
| Deneme sayısını sınırla | Sınırsız deneme bırakma |

**Parola yöneticisi** (password manager), her site için ayrı, uzun ve
rastgele bir parola üreten ve bunları şifreli bir kasada saklayan
programdır. Kullanıcı tek bir güçlü ana parola hatırlar. Tekrar kullanım
sorununun en pratik çözümü budur.

## Özet

- Parolalar çevrimiçi ve çevrimdışı tahminle, sözlük saldırısıyla, başka
  siteden sızanların denenmesiyle ve oltalamayla ele geçirilir.
- Rastgele bir parolanın entropisi `uzunluk × log2(alfabe)` bittir;
  uzunluk en çok kazandırandır.
- İnsanların seçtiği parolalar formülün söylediğinden zayıftır; bilinen
  parolalar listesiyle denetlenir.
- Rastgele kelimelerden oluşan parola cümlesi hem güçlü hem akılda kalır.
- Parola üretmek için `secrets`, `random` değil.
- İyi kural: uzunluk, sızmış parola denetimi, deneme sınırı; zorunlu
  karmaşıklık ve düzenli değiştirme yok.
