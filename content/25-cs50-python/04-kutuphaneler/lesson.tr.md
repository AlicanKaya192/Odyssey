# Kütüphaneler

CS50 Python'un beşinci haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. **Kütüphaneler** (libraries), senin ya da
başkalarının yazdığı ve programında kullanabileceğin kod parçalarıdır. Python
fonksiyonları ve özellikleri başkalarıyla **modül** (module) olarak paylaşmaya
izin verir. Eski bir projeden kod kopyalayıp yapıştırıyorsan, büyük ihtimalle
onu yeni projene getirebileceğin bir modül yapabilirsin.

## random

`random`, Python'la birlikte gelen ve kendi projene alabileceğin bir
kütüphane. Programcı olarak senden öncekilerin omuzlarında durmak daha kolay.
Bir modülü programına almak için `import` (içe aktar) yazarsın. `random`
modülünün içinde `random.choice(seq)` diye bir fonksiyon var: `random` içe
aktardığın modül, `choice` onun içindeki fonksiyon, `seq` de bir dizi (liste
gibi). `generate.py`:

```python
import random

coin = random.choice(["heads", "tails"])
print(coin)
```

```text
$ python generate.py
heads
```

Listede iki öğe olduğu için Python yazı ile turaya yüzde 50 şans verir. Her
çalıştırmada sonuç değişebilir; buradaki çıktılar örnek, seninki farklı
olabilir.

`from` ile modülün yalnızca istediğin parçasını alabilirsin. `import random`
modülün bütün fonksiyonlarını getiriyordu; yalnızca `choice`'u almak için:

```python
from random import choice

coin = choice(["heads", "tails"])
print(coin)
```

Artık `random.choice` yazmana gerek yok, yalnızca `choice`. Kod kısalır ve
okunur.

`random.randint(a, b)` `a` ile `b` arasında (ikisi dahil) rastgele bir tam
sayı üretir:

```python
import random

number = random.randint(1, 10)
print(number)
```

```text
$ python generate.py
3
```

`random.shuffle(x)` bir listeyi rastgele karıştırır:

```python
import random

cards = ["jack", "queen", "king"]
random.shuffle(cards)
for card in cards:
    print(card)
```

```text
$ python generate.py
queen
king
jack
```

`random.shuffle` kartları **yerinde** karıştırır: öteki fonksiyonların aksine
bir değer döndürmez, `cards` listesinin kendisini değiştirir. Birkaç kez
çalıştırıp sıranın değiştiğini görebilirsin.

## statistics

Python'la bir de `statistics` kütüphanesi geliyor. `mean` (ortalama) bir
değerler listesi alır ve ortalamasını verir. `average.py`:

```python
import statistics

print(statistics.mean([100, 90]))
```

```text
$ python average.py
95
```

## Komut satırı argümanları

Şimdiye kadar bütün değerleri programın içinde verdik ya da `input` ile
sorduk. Peki girdiyi **komut satırından** almak istesek? Örneğin `python
average.py` yerine `python average.py 100 90` yazıp 100 ile 90'ın ortalamasını
almak gibi.

`sys` komut satırındaki argümanları almayı sağlayan bir modül. İçindeki
`argv`, kullanıcının komut satırına yazdıklarını tutan bir liste. `name.py`:

```python
import sys

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David
hello, my name is David
```

`David` neden `sys.argv[1]`'de? Listelerin 0'dan başladığını hatırla.
`sys.argv[0]`'da ne olduğunu tahmin ettiysen: programın adı, `name.py`.

Küçük bir sorun var: kullanıcı ismi yazmazsa?

```text
$ python name.py
Traceback (most recent call last):
  File "name.py", line 3, in <module>
    print("hello, my name is", sys.argv[1])
                               ~~~~~~~~^^^
IndexError: list index out of range
```

`sys.argv[1]`'de hiçbir şey yok, çünkü hiçbir şey yazılmadı. Programı bu tür
hatadan koruyalım:

```python
import sys

try:
    print("hello, my name is", sys.argv[1])
except IndexError:
    print("Too few arguments")
```

```text
$ python name.py
Too few arguments
```

Kullanıcı ismi unutursa programı nasıl çalıştıracağına dair bir ipucu görür.
Daha savunmacı olabiliriz, fazla argümanı da yakalayalım:

```python
import sys

if len(sys.argv) < 2:
    print("Too few arguments")
elif len(sys.argv) > 2:
    print("Too many arguments")
else:
    print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David Malan
Too many arguments
```

Mantık olarak doğru. Ama hata denetimini kodun geri kalanından ayırmanın güzel
bir yanı var. `sys`'nin `exit` fonksiyonu kullanıcı bir hata yaptığında
programdan çıkmayı sağlar:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")
elif len(sys.argv) > 2:
    sys.exit("Too many arguments")

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David
hello, my name is David
```

```text
$ python name.py
Too few arguments
```

Program hata bulursa son satıra hiç gelmez. `sys.argv` kullanıcının komut
satırından bilgi vermesinin yolu, `sys.exit` de bir hata çıkınca programdan
çıkmanın yolu.

## Dilim

**Dilim** (slice), bir listenin nerede başlayıp nerede biteceğini söylemenin
yolu. Birden çok isme selam verelim:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")

for arg in sys.argv:
    print("hello, my name is", arg)
```

```text
$ python name.py David Carter Rongxin
hello, my name is name.py
hello, my name is David
hello, my name is Carter
hello, my name is Rongxin
```

İstediğimiz isimlerin yanında `hello, my name is name.py` da yazıldı. Listenin
ilk öğesini, programın adını atlamak için listeyi 1'den başlatalım:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")

for arg in sys.argv[1:]:
    print("hello, my name is", arg)
```

```text
$ python name.py David Carter Rongxin
hello, my name is David
hello, my name is Carter
hello, my name is Rongxin
```

`[1:]` "1. konumdan sona kadar" demek. Dilim her listede çalışır; başlangıç
dahil, bitiş hariç:

```python
students = ["Hermione", "Harry", "Ron", "Draco"]

print(students[1:])
print(students[:2])
print(students[1:3])
print(students[-1])
```

```text
$ python slices.py
['Harry', 'Ron', 'Draco']
['Hermione', 'Harry']
['Harry', 'Ron']
Draco
```

## Paketler

Python'un bu kadar sevilmesinin bir sebebi, işlevini genişleten güçlü
**üçüncü taraf** kütüphanelerin çokluğu. Klasör olarak gelen bu kütüphanelere
**paket** (package) denir. **PyPI** bugün bulunabilen bütün üçüncü taraf
paketlerin dizinidir. Python'un paket yöneticisi `pip` bir paketi hızlıca
kurar:

```text
pip install cowsay
```

`cowsay` kullanıcıya bir ineğin konuşmasını sağlayan ünlü bir paket. Odyssey'de
kurulu geliyor; bilgisayarında kendi projelerinde kullanmak istersen yukarıdaki
komut yeter. `say.py`:

```python
import cowsay
import sys

if len(sys.argv) == 2:
    cowsay.cow("hello, " + sys.argv[1])
```

```text
$ python say.py David
  ____________
| hello, David |
  ============
            \
             \
               ^__^
               (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||
```

Program önce kullanıcının komut satırına tam bir argüman yazdığını denetler
(`sys.argv` iki öğeli: programın adı ve o argüman), sonra inek konuşur.
`cowsay.cow` yerine `cowsay.trex` yazarsan bir T-rex konuşur.

## API'ler

**API'ler** (application programming interface, uygulama programlama
arayüzü) başkalarının koduna bağlanmanı sağlar. `requests` paketi programının
bir web tarayıcısı gibi davranmasını sağlar. Apple'ın iTunes'unun bir API'si
var; derste David şu adresin bir şarkı arayıp cevabı **JSON** biçiminde
verdiğini gösteriyor: `https://itunes.apple.com/search?entity=song&limit=1&term=weezer`.
JSON, uygulamalar arasında veri taşımak için kullanılan metin tabanlı bir
biçim; Python onu sözlüklere ve listelere çevirebiliyor.

```python
import json
import requests
import sys

if len(sys.argv) != 2:
    sys.exit()

url = "https://itunes.apple.com/search?entity=song&limit=50&term="
response = requests.get(url + sys.argv[1])

o = response.json()
for result in o["results"]:
    print(result["trackName"])
```

Bu kod internete bağlandığı için burada çalıştırılmadı; videoda çıktısını
görebilirsin. `response.json()` cevabı bir sözlüğe çevirir; `results`
anahtarında sözlüklerden oluşan bir liste var, her birinde `trackName`.

Python'un yerleşik `json` kütüphanesi bu veriyi okumayı kolaylaştırır:
`json.dumps(..., indent=2)` onu girintili, okunur bir metne çevirir. Aynı
biçimde yerel bir örnek veriyle:

```python
import json

data = {
    "resultCount": 2,
    "results": [
        {"trackName": "Track One", "artistName": "Band"},
        {"trackName": "Track Two", "artistName": "Band"},
    ],
}

print(json.dumps(data["results"][0], indent=2))

for result in data["results"]:
    print(result["trackName"])
```

```text
$ python itunes.py
{
  "trackName": "Track One",
  "artistName": "Band"
}
Track One
Track Two
```

İnternete çıkan bir alıştırmayı Odyssey kendi **alıştırma sunucusuyla**
yapıyor: bu haftanın problem setindeki Bitcoin fiyatı sorusu gerçek bir API
gibi cevap veren, ama bilgisayarından çıkmayan bir adrese istek atıyor.

## Kendi kütüphaneni yapmak

Python programcısı olarak kendi kütüphaneni de yapabilirsin; bir kod
parçasını tekrar tekrar kullanmak ya da başkalarıyla paylaşmak istediğinde.
"Merhaba" ve "hoşça kal" diyen bir modül, `sayings.py`:

```python
def hello(name):
    print(f"hello, {name}")


def goodbye(name):
    print(f"goodbye, {name}")
```

Bu kod tek başına kullanıcı için hiçbir şey yapmaz. Ama başka bir programcı
onu içe aktarırsa bu fonksiyonları kendi kodunda kullanabilir. `say.py`:

```python
import sys

from sayings import goodbye

if len(sys.argv) == 2:
    goodbye(sys.argv[1])
```

```text
$ python say.py David
goodbye, David
```

`from sayings import goodbye` `sayings` modülünden `goodbye`'ı alır; modülün
adı dosyanın adı, `.py` olmadan.

## Özet

Kütüphaneler Python'un yeteneklerini genişletir. Bazıları Python'la gelir,
yalnızca içe aktarılır; bazıları `pip` ile kurulan üçüncü taraf paketlerdir;
kendininkini de yapabilirsin:

- `import` ve `from ... import ...`
- `random`: `choice`, `randint`, `shuffle`
- `statistics.mean`
- `sys.argv`, `sys.exit` ve komut satırı argümanları
- Dilim: `[1:]`, `[:2]`, `[1:3]`
- Paketler, PyPI ve `pip`
- API'ler, `requests` ve JSON
- Kendi modülün

## Bu haftanın problem seti

**Alıştırma** sekmesindeki yedi alıştırma bu dersin konularını tek tek
çalıştırıyor. **Problem Seti** sekmesindeki altısı CS50'nin bu haftaki ödevi
(Problem Set 4):

| Problem | Ne istiyor | Dersteki konu |
|---|---|---|
| Emojize | `:thumbs_up:` → emoji | paket (`emoji`) |
| Frank, Ian ve Glen'in Harfleri | büyük harfli yazı | paket (`pyfiglet`), `sys.argv`, `sys.exit` |
| Adieu, Adieu | isimleri `a, b, and c` diye birleştirmek | paket (`inflect`), `EOFError` |
| Tahmin Oyunu | rastgele sayıyı bulmak | `random.randint`, yeniden sormak |
| Küçük Profesör | on toplama sorusu | `random`, fonksiyonlar |
| Bitcoin Fiyat Endeksi | API'den fiyat almak | `requests`, JSON, `sys.argv` |

Paketlerin her biri yönergede ipucuyla anlatılıyor; CS50 de öğrenciyi paketin
belgesine yolluyor.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 4. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
