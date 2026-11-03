# Rastgelelik

XOR ve Tek Kullanımlık Şifre bölümünde tek kullanımlık şifrenin ilk koşulu
"anahtar gerçekten rastgele" idi. Parolalar bölümünde parolayı `random`
ile değil `secrets` ile ürettik ve ayrıntısını buraya bıraktık. Bu bölüm
rastgeleliğin kriptografide neden bu kadar önemli olduğunu, iki tür
rastgele sayı üretecini, doğru kaynağın Python'da nasıl kullanıldığını ve
rastgele sayıyı kullanırken yapılan sessiz bir hatayı anlatıyor.

## Kriptografi neden rastgeleliğe dayanır?

Kriptografi Nedir? bölümündeki Kerckhoffs ilkesini hatırla: algoritma
herkese açıktır, gizli olan yalnızca **anahtardır**. Anahtar tahmin
edilebiliyorsa en sağlam algoritma da hiçbir şey korumaz. Bir sistemde
rastgele üretilmesi gereken değerler yalnızca anahtarlar da değildir:

| Değer | Ne işe yarar? | Tipik boyut |
|---|---|---|
| Anahtar (key) | Şifreleme ve HMAC'in gizli girdisi | 128 ya da 256 bit |
| Nonce / IV | Aynı anahtarla her mesajı farklı şifrelemek | 96 ya da 128 bit |
| Tuz (salt) | Aynı parolaların özetini farklı kılmak | 128 bit |
| Jeton (token) | Oturum kimliği, parola sıfırlama bağlantısı, API anahtarı | 128 bit ve üstü |

Bu değerlerin ortak şartı **tahmin edilememek**. "Rastgele görünmek" yetmez:
dışarıdan bakan biri bir sonraki değeri önceki değerlerden çıkaramamalı.

## İki tür üreteç

Bilgisayar kendi başına rastgele bir şey yapmaz; her adımı bir kurala
uyar. Rastgele sayılar iki yoldan gelir:

- **Sözde rastgele sayı üreteci** (pseudo-random number generator, PRNG):
  bir başlangıç değerinden, **tohumdan** (seed), matematiksel bir kuralla
  sayı dizisi üretir. Dizi rastgele görünür ve istatistik testlerinden
  geçer, ama tohum aynıysa dizi de aynıdır. Python'un `random` modülü
  böyledir (Mersenne Twister adlı bir algoritma); benzetim, oyun ve
  örneklem için yazılmıştır.
- **Kriptografik rastgele sayı üreteci** (cryptographically secure PRNG,
  CSPRNG): işletim sisteminin donanımdan ve olaylardan topladığı gürültüyle
  beslenir ve çıktısını görmek sonrakini tahmin etmeye yaramaz. Python'da
  `secrets` modülü ve `os.urandom` bunu kullanır (Windows'ta
  `BCryptGenRandom`, Linux'ta `getrandom`).

## Aynı tohum, aynı dizi

`random` modülünün **belirlenimci** (deterministic) olduğunu görmek için
aynı tohumu iki kez verelim:

```python
import random

random.seed(42)
first = [random.randint(0, 99) for _ in range(5)]
random.seed(42)
second = [random.randint(0, 99) for _ in range(5)]
print(first)
print(first == second)
```

```text
[81, 14, 3, 94, 35]
True
```

Bu bilgisayarda da senin bilgisayarında da aynı beş sayı çıkar. Benzetim
için bu bir özelliktir: deneyi tekrarlayabilirsin. Güvenlik için ise tam
tersi: tahmin edilebilir bir üretecin çıktısı da tahmin edilebilir. Savunma
basittir: anahtar, jeton, tuz ya da parola **hiçbir zaman** `random` ile
üretilmez; tohum vermemek de yetmez, çünkü üretecin kendisi kriptografik
değildir. Bu işler `secrets` ile yapılır.

## `secrets` modülü

`secrets` tam bu iş için yazılmıştır ve birkaç kısa fonksiyonu vardır:

```python
import secrets

token = secrets.token_hex(16)
link = secrets.token_urlsafe(16)
print(len(token), all(c in "0123456789abcdef" for c in token))
print(len(link))
print(secrets.token_hex(16) == secrets.token_hex(16))
code = secrets.randbelow(1_000_000)
print(0 <= code < 1_000_000)
print(secrets.choice(["red", "green", "blue"]) in ["red", "green", "blue"])
```

```text
32 True
22
False
True
True
```

Çıktıda jetonların kendisini değil **özelliklerini** yazdırdık, çünkü
değerler her çalıştırmada değişir; ölçülebilen tek şey özellikleridir.

- `token_hex(16)`: 16 rastgele bayt, onaltılık yazımla 32 karakter.
- `token_urlsafe(16)`: aynı 16 bayt, bağlantıya konabilecek Base64
  yazımıyla 22 karakter. İkisi de 128 bit taşır; uzunluk farkı yalnızca
  yazımdan gelir.
- İki ayrı `token_hex(16)` çağrısı birbirine eşit çıkmadı.
- `randbelow(n)`: `0` ile `n - 1` arasında bir tam sayı (ör. altı haneli
  doğrulama kodu).
- `choice(dizi)`: diziden bir öğe (ör. parola karakteri).

Ham bayt gerektiğinde (anahtar, nonce, tuz) `secrets.token_bytes(n)` ya da
`os.urandom(n)` kullanılır; ikisi aynı kaynaktan okur:

```python
import os
import secrets

key = os.urandom(32)
nonce = secrets.token_bytes(12)
salt = secrets.token_bytes(16)
print(len(key) * 8, len(nonce) * 8, len(salt) * 8)
```

```text
256 96 128
```

256 bitlik anahtar, 96 bitlik nonce, 128 bitlik tuz: yukarıdaki tablonun
boyutları.

## Kaç bit yeter?

Parolalar bölümündeki formül jetonlar için de geçerlidir: alfabede `a`
farklı karakter varsa ve her karakter bağımsız ve rastgele seçildiyse,
`n` karakterlik jeton `n × log2(a)` bit taşır.

```python
import math


def entropy_bits(alphabet_size, length):
    return length * math.log2(alphabet_size)


cases = [("6 digits", 10, 6), ("16 of 62 chars", 62, 16), ("32 hex chars", 16, 32)]
for name, size, length in cases:
    print(f"{name:<15} {entropy_bits(size, length):6.1f} bits")
```

```text
6 digits          19.9 bits
16 of 62 chars    95.3 bits
32 hex chars     128.0 bits
```

62 karakterlik alfabeden (harf ve rakam) 16 karakter 95,3 bit eder.
Altı haneli bir kod ise yalnızca 19,9 bit: bu yüzden doğrulama kodları kısa
ömürlü tutulur ve deneme sayısı sınırlanır.

Uzun ömürlü jetonlar için yaygın hedef **128 bit**tir: ortalama `2^127`
deneme gerektirir. Bir alfabeyle bu hedefe kaç karakterde ulaşılır?

```python
import math

for size in [10, 16, 62, 64]:
    print(size, "->", math.ceil(128 / math.log2(size)), "chars for 128 bits")
```

```text
10 -> 39 chars for 128 bits
16 -> 32 chars for 128 bits
62 -> 22 chars for 128 bits
64 -> 22 chars for 128 bits
```

Sonuç yukarı yuvarlanır (`math.ceil`): 62 karakterde hesap 21,5 çıkıyor ve
21 karakter hedefin altında kalır. 64 karakterlik Base64 alfabesinde de 22
karakter gerekiyor; `token_urlsafe(16)`'nın uzunluğu buradan geliyor.

## Modulo yanlılığı

Doğru kaynağı seçmek yetmez; rastgele sayıyı **nasıl kullandığın** da
önemlidir. Bir bayt 0 ile 255 arasında, her değeri eşit olasılıkla verir.
0–99 arasında bir sayı isteyen biri `bayt % 100` yazabilir. Her olası baytı
bir kez sayalım:

```python
from collections import Counter

counts = Counter(b % 100 for b in range(256))
print("value 7: ", counts[7], "of 256")
print("value 70:", counts[70], "of 256")
print("values seen 3 times:", sum(1 for v in range(100) if counts[v] == 3))
```

```text
value 7:  3 of 256
value 70: 2 of 256
values seen 3 times: 56
```

256, 100'e tam bölünmez: 200'e kadarki baytlar her sonucu ikişer kez
verir, artan 56 bayt (200–255) da 0–55'i bir kez daha verir. 0–55 arası
sonuçlar 70 gibi sonuçlardan **bir buçuk kat** daha sık çıkar. Buna
**modulo yanlılığı** (modulo bias) denir. Üretilen sayı artık eşit
dağılmaz; bir kod ya da anahtar uzayının bir kısmı ötekinden daha olası
olur.

Doğrusu, eşit bölünmeyen artığı **atıp** yeniden çekmektir. Kuralı yine
bütün baytları sayarak görelim:

```python
from collections import Counter


def fair_values(n):
    limit = 256 - 256 % n
    return [b % n for b in range(256) if b < limit]


counts = Counter(fair_values(100))
print(len(counts), set(counts.values()))
print(256 - 256 % 100, "kept,", 256 % 100, "thrown away")
```

```text
100 {2}
200 kept, 56 thrown away
```

Kalan 200 baytta her sonuç tam iki kez çıkıyor. Bu kuralı her seferinde
kendin yazma: `secrets.randbelow(n)` aynı şeyi senin yerine doğru yapar.

## Kendi üretecini yazma

Kriptografi Nedir? bölümünde kendi şifreleme algoritmanı yazmamayı
gördük; aynısı burada da geçerli: **kendi rastgele sayı üretecini yazma.**
Saatten tohum almak, saatin özetini almak, birkaç
değişkeni karıştırmak ya da ders kitabından bir formül kopyalamak rastgele
**görünen** ama tahmin edilebilen sayılar verir. İşletim sisteminin
kaynağı yıllarca incelenmiştir ve tek çağrıyla kullanılır:

| İş | Kullan | Kullanma |
|---|---|---|
| Jeton, oturum kimliği | `secrets.token_urlsafe(32)` | `random.random()`, saat |
| Anahtar, nonce, tuz | `secrets.token_bytes(n)`, `os.urandom(n)` | `random.randbytes(n)` |
| Aralıkta sayı | `secrets.randbelow(n)` | `bayt % n`, `random.randint` |
| Listeden seçim | `secrets.choice(dizi)` | `random.choice(dizi)` |
| Benzetim, oyun, örneklem | `random` (tohumla tekrarlanabilir) | — |

`random` kötü bir modül değildir; yalnızca güvenlik için yazılmamıştır.
Tekrarlanabilir bir deney istiyorsan doğru araç odur.

## Kodda yanlış kaynağı bulmak

Kod incelemesinde (Sistem Güvenliği ve Operasyon modülünün Kod İnceleme ve
Statik Analiz bölümü) aranan ilk şeylerden biri güvenlik değerlerinin
`random` ile üretilmesidir. Basit bir denetleyici satırlarda `random.`
kullanımını arayabilir:

```python
SOURCE = """import random
import secrets
token = secrets.token_hex(16)
reset_code = random.randint(100000, 999999)
session_id = str(random.random())
color = secrets.choice(["a", "b"])
"""


def find_weak(lines):
    return [i for i, line in enumerate(lines, 1) if "random." in line]


print(find_weak(SOURCE.splitlines()))
```

```text
[4, 5]
```

Denetleyici parola sıfırlama kodunun (4. satır) ve oturum kimliğinin (5.
satır) `random` ile üretildiğini buldu. İkisi de `secrets` ile yeniden
yazılır. Bu kadar basit bir arama yanlış alarm da verir: yorum satırındaki
`random.` ya da güvenli `random.SystemRandom` da yakalanır. Alıştırmada
denetleyiciyi bunları ayıracak kadar geliştireceksin.

## Özet

- Anahtar, nonce, tuz ve jetonun ortak şartı **tahmin edilememek**.
- `random` **sözde rastgele** ve belirlenimcidir: aynı tohum aynı diziyi
  verir. Benzetim için iyi, güvenlik için kullanılmaz.
- Güvenlik için `secrets` (`token_hex`, `token_urlsafe`, `token_bytes`,
  `randbelow`, `choice`) ya da `os.urandom`.
- Entropi `n × log2(a)` bit; uzun ömürlü jeton için hedef 128 bit, uzunluk
  `math.ceil` ile yukarı yuvarlanır.
- `bayt % n` sonucu eşit dağıtmaz (**modulo yanlılığı**); `randbelow` kullan.
- Kendi rastgele üretecini yazma; işletim sisteminin kaynağını kullan.
