# Dosya İşlemleri

CS50 Python'un yedinci haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. Şimdiye kadar yazdığımız programların hepsi
bilgiyi **bellekte** (memory) tuttu: değişkenler, listeler, sözlükler. Program
bitince hepsi kayboluyor. **Dosya işlemleri** (file I/O, input/output yani
girdi/çıktı), programın bir dosyadan okuması ya da bir dosyaya yazması
demek. Dosyaya yazılan bilgi program kapandıktan sonra da kalır.

## Bellekte kalan liste

Üç isim soran, sıralayıp selam veren bir program, `names.py`:

```python
names = []

for _ in range(3):
    names.append(input("What's your name? "))

for name in sorted(names):
    print(f"hello, {name}")
```

```text
$ python names.py
What's your name? Hermione
What's your name? Harry
What's your name? Ron
hello, Harry
hello, Hermione
hello, Ron
```

`sorted` listeyi abece sırasına koyuyor. Program çalışıyor ama bir kusuru
var: kapandığı anda üç isim de gidiyor. Yarın yeniden çalıştırsan baştan
sormak zorunda. İsimleri bir dosyada saklayalım.

## open

`open`, Python'un hazır fonksiyonu: bir dosyayı okumak, yazmak ya da sonuna
eklemek için açar. İlk denemede tek bir isim soralım ve dosyaya yazalım:

```python
name = input("What's your name? ")

file = open("names.txt", "w")
file.write(name)
file.close()
```

`open("names.txt", "w")` iki argüman alıyor: dosyanın adı ve **kip** (mode).
`"w"` yazma (write) kipi: dosya yoksa oluşturur. `file.write(name)` ismi
dosyaya yazar, `file.close()` dosyayı kapatır. Programı iki kez çalıştırıp
dosyanın içine bakalım (`cat` dosyanın içini terminale yazan komut; Windows'un
komut isteminde aynı işi `type` yapıyor, istersen dosyayı editörde de
açabilirsin):

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ cat names.txt
Harry
```

`Hermione` nerede? `"w"` kipi dosyayı her açılışta **sıfırdan** yazıyor;
ikinci çalıştırma birincinin yazdığını sildi. Var olan bilginin sonuna eklemek
için **ekleme** (append) kipi `"a"`:

```python
name = input("What's your name? ")

file = open("names.txt", "a")
file.write(name)
file.close()
```

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ python names.py
What's your name? Ron
$ cat names.txt
HermioneHarryRon
```

Üç isim de dosyada ama birbirine yapışık. `write` yalnızca ona verdiğini
yazıyor; `print` gibi kendiliğinden satır sonu eklemiyor. Satır sonunu (`\n`)
kendimiz ekleyelim:

```python
name = input("What's your name? ")

file = open("names.txt", "a")
file.write(f"{name}\n")
file.close()
```

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ python names.py
What's your name? Ron
$ cat names.txt
Hermione
Harry
Ron
```

Her isim artık kendi satırında.

## with

`file.close()` yazmayı unutmak kolay; kapatılmayan dosyaya yazılanlar
kaybolabilir. Python bunun için `with` anahtar kelimesini veriyor: dosyayı
açar, girintili blok bitince **kendiliğinden** kapatır.

```python
name = input("What's your name? ")

with open("names.txt", "a") as file:
    file.write(f"{name}\n")
```

`as file` açılan dosyaya bir ad veriyor. Blok bitince Python dosyayı
kapatıyor; `close` yazmamıza gerek kalmıyor.

## Dosyadan okumak

Yazdığımızı okuyalım. `"r"` okuma (read) kipi; `readlines` dosyanın bütün
satırlarını bir liste olarak verir:

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line)
```

```text
$ python names.py
hello, Hermione

hello, Harry

hello, Ron
```

Satırların arasında neden boş satırlar var? Dosyadaki her satır `\n` ile
bitiyor ve `print` kendi satır sonunu da ekliyor: iki satır sonu. Metnin
sonundaki boşlukları ve satır sonunu `rstrip` ile atalım:

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line.rstrip())
```

```text
$ python names.py
hello, Hermione
hello, Harry
hello, Ron
```

Daha kısası da var. Dosyanın üstünde doğrudan döngü kurulabilir; her turda
bir satır gelir, `readlines` gerekmez. Okuma kipi de varsayılan olduğu için
`"r"` yazılmayabilir:

```python
with open("names.txt") as file:
    for line in file:
        print("hello,", line.rstrip())
```

```text
$ python names.py
hello, Hermione
hello, Harry
hello, Ron
```

İsimleri sıralı göstermek için önce bir listeye toplayalım, sonra sıralayalım:

```python
names = []

with open("names.txt") as file:
    for line in file:
        names.append(line.rstrip())

for name in sorted(names):
    print(f"hello, {name}")
```

```text
$ python names.py
hello, Draco
hello, Harry
hello, Hermione
hello, Ron
```

Dosya döngüyle gezilebildiği için doğrudan `sorted`'a da verilebilir:
`for line in sorted(file):`. Ters sıra için `sorted(names, reverse=True)`.

## CSV

İsimden fazlasını saklamak istersek? Öğrencilerin adlarını ve binalarını
tutalım. Yaygın bir yöntem **CSV** (comma-separated values, virgülle ayrılmış
değerler): her satır bir kayıt, alanlar virgülle ayrılmış. `students.csv`:

```text
Hermione,Gryffindor
Harry,Gryffindor
Ron,Gryffindor
Draco,Slytherin
```

Her satırı virgülden bölelim (`split(",")`):

```python
with open("students.csv") as file:
    for line in file:
        row = line.rstrip().split(",")
        print(f"{row[0]} is in {row[1]}")
```

```text
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

`row` iki öğeli bir liste: `row[0]` ad, `row[1]` bina. Python'da bir listeyi
doğrudan iki değişkene **açabiliriz** (unpack): `name, house =
line.rstrip().split(",")`. Kod okunur hâle geliyor:

```python
with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        print(f"{name} is in {house}")
```

```text
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

### Sözlükleri sıralamak

Cümleleri öğrencinin adına göre sıralı yazmak istersek, metinleri değil
öğrencileri sıralamamız gerekiyor. Her öğrenciyi bir sözlük yapıp listeye
koyalım. Sözlükleri karşılaştırmayı Python bilmiyor; `sorted`'a neye göre
sıralayacağını `key` argümanıyla söyleriz. `key`'e bir **fonksiyon**
veririz: bir öğrenci alıp sıralamada kullanılacak değeri döndürür:

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        student = {"name": name, "house": house}
        students.append(student)


def get_name(student):
    return student["name"]


for student in sorted(students, key=get_name):
    print(f"{student['name']} is in {student['house']}")
```

```text
$ python students.py
Draco is in Slytherin
Harry is in Gryffindor
Hermione is in Gryffindor
Ron is in Gryffindor
```

`key=get_name` yazarken `get_name()` yazmadık: fonksiyonu çağırmıyoruz,
`sorted`'a veriyoruz; her öğrenci için o çağıracak. Yalnızca bu iş için
adlı bir fonksiyon yazmak uzun geliyorsa **lambda** var: adı olmayan, tek
ifadelik fonksiyon. `lambda student: student["name"]` "bir öğrenci al, adını
döndür" demek:

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        students.append({"name": name, "house": house})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['house']}")
```

Çıktı aynı. Bina adına göre sıralamak için `student["house"]` yeter.

### Alanın içinde virgül

Şimdi bina yerine öğrencilerin evini tutalım. Harry'nin evi "Number Four,
Privet Drive"; adreste virgül var. CSV bu durumda alanı tırnağa alır:

```text
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

`split(",")` tırnağı bilmiyor, Harry'nin satırını üç parçaya bölüyor:

```python
with open("students.csv") as file:
    for line in file:
        name, home = line.rstrip().split(",")
        print(f"{name} is from {home}")
```

```text
$ python students.py
Traceback (most recent call last):
  File "students.py", line 3, in <module>
    name, home = line.rstrip().split(",")
    ^^^^^^^^^^
ValueError: too many values to unpack (expected 2, got 3)
```

Bu işi elle çözmeye çalışmak yerine Python'un **`csv`** kütüphanesini
kullanalım. `csv.reader` tırnakları ve içlerindeki virgülleri doğru okur, her
satırı bir liste olarak verir:

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.reader(file)
    for name, home in reader:
        students.append({"name": name, "home": home})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

```text
$ python students.py
Draco is from Malfoy Manor
Harry is from Number Four, Privet Drive
Ron is from The Burrow
```

### DictReader

CSV dosyalarının çoğunun ilk satırı **başlık** (header): sütunların adları.
`students.csv`'nin başına `name,home` ekleyelim:

```text
name,home
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

`csv.DictReader` başlığı okur ve her satırı, sütun adlarını anahtar yapan bir
sözlük olarak verir:

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({"name": row["name"], "home": row["home"]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

```text
$ python students.py
Draco is from Malfoy Manor
Harry is from Number Four, Privet Drive
Ron is from The Burrow
```

Bunun bir faydası daha var: biri dosyadaki sütunların yerini değiştirirse
(`home,name`), program yine çalışır, çünkü sütunları sıraya göre değil adına
göre okuyoruz.

## CSV'ye yazmak

Kullanıcıdan ad ve ev alıp `students.csv`'nin sonuna ekleyelim. `csv.writer`
her satırı bir listeden yazar ve virgül içeren alanı kendisi tırnağa alır:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])
```

Bu bilgisayarda (Windows) iki kez çalıştırıp dosyaya bakalım:

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"

Ron,The Burrow
```

Tırnaklar yerinde, ama satırların arasında boş satır var. Sebep Windows:
`csv.writer` her satırı `\r\n` ile bitiriyor, Windows'ta metin kipinde açılan
dosya da her `\n`'yi `\r\n`'ye çeviriyor; satır `\r\r\n` ile bitiyor ve okuyan
iki satır sonu görüyor. Python'un belgesi CSV dosyasını `newline=""` ile
açmayı söylüyor: dosya satır sonlarına dokunmuyor, işi `csv`'ye bırakıyor.
CS50 Linux'ta çalıştığı için bu sorunu görmüyor; Windows'ta çalışan biz
CSV'ye yazarken hep `newline=""` yazacağız:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])
```

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"
Ron,The Burrow
```

Boş satırlar yalnızca görüntü sorunu değil. `newline=""` olmadan yazılmış bu
dosyayı `csv.reader` okuyunca boş satırlar boş liste (`[]`) olarak geliyor ve
`for name, home in reader:` ilk boş satırda `ValueError` veriyor;
`DictReader` boş satırları atladığı için onda sorun görünmüyor. Sorunu
yazarken çözmek en temizi.

### DictWriter

`csv.DictWriter` satırı sözlükten yazar; sütunların sırasını `fieldnames`
belirler. Sözlükteki anahtarların sırası önemli değil:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "home"])
    writer.writerow({"home": home, "name": name})
```

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"
Ron,The Burrow
```

Dosya boşsa önce `writer.writeheader()` başlık satırını yazar; problem
setinde kullanacaksın.

## İkili dosyalar ve PIL

Metin dosyaları okunabilir karakterlerden oluşur. **İkili** (binary)
dosyalar ise yalnızca birler ve sıfırlardan: resim, ses, video. Onları da
okuyup yazabiliriz, ama içlerini anlamak için o biçimi bilen bir kütüphane
gerekir. Resimler için yaygın olanı **Pillow**; programda `PIL` adıyla içe
aktarılıyor (`pip install Pillow`, Odyssey'de kurulu).

Elimizde bir karakterin iki **kostümü** olsun: `costume1.gif` ve
`costume2.gif`. İkisinden, kostümler arasında gidip gelen tek bir hareketli
GIF yapalım. Dosyaların adlarını komut satırından alıyoruz, `costumes.py`:

```python
import sys

from PIL import Image

images = []

for arg in sys.argv[1:]:
    image = Image.open(arg)
    images.append(image)

images[0].save(
    "costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0
)
```

```text
$ python costumes.py costume1.gif costume2.gif
```

`Image.open` resmi açar. Hareketli GIF'i ilk resmin `save` metodu yazıyor:
`save_all=True` birden çok kare, `append_images` ilk karenin arkasına eklenen
kareler, `duration=200` her karenin ekranda kalacağı süre (milisaniye),
`loop=0` sonsuz döngü. Sonuç:

<figure class="fig"><div class="versus"><div><h5>costume1.gif</h5><img src="data:image/gif;base64,R0lGODdheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACwAAAAAeAB4AEAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFiw4FaNzIsaNHjCBDQvRIsqRJkiJTYjwJoCUAAjAJuNzo8mXMmSZV6hx5sqfPnjuDPvwZk0DHoj+FKkX4s6nTnEtDPp1KtWlUhlWzaq2q1CfBrWCffvV6EWXDsGg/nj159WBarW3jDphLt65dk3bz1o3Ld6DevAv/2u1LuLDhw4gTS3zLUXHUnjUBmIwM1LFIyC5h4qSZWWbLypZBMk4aeuXoqaUjnkabeuzq12rjwp6dVSpog7TDJiRLOLdTihtLd7xLlXjw1iAF/yWpXC/y59CjS59Ovbp1w1CvP06r3TTs7jx9a/8Ev5Bl5M0az6OPTb6geZtFP6dvWVSz5OztB/6kXJL/7fwCidcRgG71FJOBRvFGoH5T1QcTVQsGICBb5E1IGnUW1tZahm8pxuFrfX0ooFCkiSiWhApalGKAJq6IIoUT/Ydbi/gxJeNQ44VHY444DogdjRFyGKFBzc3VU5EDDEkkknQxx+RcShL0ZEJTRonQYBJhaeWWXHbp5ZdghinmmGSWuaFVZioEVpoMdkjmd2D65uWIW1poJWb+caTejflNVpN98gkQGaD3mRWkn/DdVGhn8RVqKIHvJbrZn4o6yh6APu3pkaYwQvqhkkKCmuGdE3Lp04ElodqpqEQ5iBSaQ4qguOCOfe4oQIW28mhdro1Vx+ujyP26qmXCXuhYsb8lhixqPy4LIV/OrrldtLoFlRS1txprG4zYtjkscDJGO+O3OpZk47Ln1pgRn97+Wh67apr7brFYuVjvcWu5uy6wiy3Gq7/49mZrRbcqC6SnocZaqqkCCOaUwwVz+SReTEr85ABOVhnlxRh7xPGWHy+p8cYVX1myl4I9lDKbLLfsckoBAQA7" alt="costume1.gif" width="120" height="120"></div><div><h5>costume2.gif</h5><img src="data:image/gif;base64,R0lGODdheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACwAAAAAeAB4AEAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFiw4FaNzIsaNHjCBDQvRIsqRJkiJTYjwJoCUAAjAJuNzo8mXMmSYtnlSZ8aTPnz4f/uRZEWhMAh2PAl04lChFoFCjSt3o9OnUq1hRVo2YtatXrVsPNhX4tSzUsAbBMjXLlipap22zvp0rcIDdu3jzmszLFy/dvwP78l0oOC/gw4gTK17MWGJct423+qwJwCTloCEhJ57sEiZOmp1ltsQ8kvTmx6YTjm2MeurApZFft44bm+zs24tv61YbdnXB3WVr9wQOW3hRjnqvJtds/GJhwSSf921Ovbr169iza99uPCf3uW2/g//cLZ4rceblxVqm/Fkj+/YfL/L+y7LlUc+V3du/P9q749Tg/XRZSQMCqFBxp52HHkK+MfZTTD7BhCCDBjo41X0SupZWhRYqWFIADcbmoVzUjUhidyZ2hWKKX7HGYniIwfaiVICFOOOEve104I3+Hbbgjjz+qF2Q6ak3YpEMSWeXT0oOgGSSTd4VXZR2PakQlQlhaaVDhknU5ZZghinmmGSWaeaZaKap5po+nsWmUF69SSGMcuK2JnFpKnjmkSIJEBlnBXL0HoelCRkgSZTh158AiYq2aHw6zXcoovsdtWholub3oVU60rdepY6CBip8HU0U4lsCskdpoJvCSWiOKRay2mOCHro6q2KxMnQqrrWu9SqtJUEYbIadqvYrsCdheF9UxhYr3Iu/HRsjjyDu2mGQzj6Lbbbabitpbd7eCm643/5JbqsrngvpuOqKi2y76/IKr7RVzevmtEHZ6ye+/unbZrbz1lhhwJOiayS5/8Z7cLjA2rqtg/89nJ7ERRK5JbRj8mmmRoVF1fG+Z1K5V5QhUznAlFqSafLJHq1spssGwVxmyjGTrGZhD+Es584899xYQAA7" alt="costume2.gif" width="120" height="120"></div><div><h5>costumes.gif</h5><img src="data:image/gif;base64,R0lGODlheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQAFAAAACwAAAAAeAB4AAAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFixgzatzIsaPHjyBDihxJsqTJkyhTqlzJsqXLlzBjypxJs6bNmzhz6swooKdPnztj/hxKNKhKokiTGi2ZtGnRpSCdSn0KdePUqz+rasTKtafWi13DfqUYtuzYiGXTnn2Y1uxahm3Vvk0Yt+1chHXl3i0oFYBfv03/Ana6l69TwX+RIh7ctPDAw4sZ94wsmWrhwIIJEBDsE7FmzkodQ/ar+TPjzKUTN76MGUDp1AA6k369OfbqvaNp15btmnbloaJb9zZtWwBq4oRZC0f+E7Xq23enRla8eGrwvqCpP0+OO2/c697dKv8Pz9WxQPJizaPvav78euvtA7yH335qaamar8Z37/R+Uv/cxXfVa0MRSF99WOlGW3kIdqWgeN3Np1+EEk74VoXprYUhexpuyOFYHn6oVYgZVkWiiEudWKJRKqKoU4t65QSjXTLOSKNNNtaFY446zsSjdz7+mJdQQg75UpHhuYQkeSwtid5RTj55UpTvmUTlfCRdKaFIWlYYlXVdAmehVfCFmZV8B/Ik1WNmesVfgGCtyWabBI1ZUZpohmkQnhLxSeeecpIVqGF6HsRnQ4fm2SVdgzqU6JtULvQoXnACqiVcjSIamkKFcjqpoZZ5Gqmm0EEEnKNXsrXpRECZGiVaobKT2uersLa6kpOCCqDkknfChORcvwL743gwqjejgC3up6gAAzTbbFrOPnumsj1Fay1X1kbrprIBZOutVN5my2234WbbVLniKovutUmtG6267mpLVLzvxkevs0jd2+x++g6Qr7786vvvvQETbFC/8MabkMEFu7swveMqrJDE45Lr7UPlVnxwvRFZq/HHIIcs8sgkkxQQACH5BAEUAAgALFYAGwAeAEMAgv////r27Hxc3FpAtB4eKAAAAAAAAAAAAAjMABEIHEiwoEGBAg4qXEhQgEOGEAs6nBgx4sSLFRlexJjR4MaNHRt+BBlyJMmOJjmiTPmwJMuWGV/CjPkyJAKZNnG6ZJmz5s6UPX2u5PnTZFCgRUceNZr041KmNIVGRdpUZdWZT7FmtXnwJFeRFL92TSi2bMgAAcwaRJtW7UC2bd3CjWt2Lt2yc90isCuXb127d20CRot3cOCMhglzTaz4LOPDEB9DZih58WPLjDEb/npZ82DOmT0DBp1Y9GjBpUn7FXv6L1u9exvrhRwQADs=" alt="costumes.gif" width="120" height="120"></div></div><figcaption>İki kostüm ve onlardan yapılan hareketli GIF (sağdaki el sallıyor).</figcaption></figure>

## Özet

Bu hafta programların dosyalarla konuşmasını gördük:

- `open` ve kipleri: `"r"` oku, `"w"` sıfırdan yaz, `"a"` sona ekle
- `with`: dosya blok bitince kendiliğinden kapanır
- Okurken satırların `\n`'si: `rstrip`
- CSV: `csv.reader`, `csv.DictReader`, `csv.writer`, `csv.DictWriter`;
  Windows'ta yazarken `newline=""`
- `sorted(..., key=...)` ve `lambda`
- İkili dosyalar ve `PIL` ile resim

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 6. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
