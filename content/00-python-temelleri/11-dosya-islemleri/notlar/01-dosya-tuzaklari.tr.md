Dosya işlemlerinde hatalar pahalı: çoğu hata vermiyor, sessizce **veri
kaybettiriyor**. Aşağıdakiler en sık düşülenler.

## 1. `"w"` dosyayı siliyor

En pahalı tuzak bu.

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("new line\n")
```

`results.txt` içinde bir aylık kayıt varsa hepsi gitti. `"w"` dosyayı açar
açmaz içeriği sıfırlıyor — sen daha `write` bile çağırmadan.

Bir dosyaya ekleme yapacaksan `"a"` kullan:

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("new line\n")
```

Emin değilsen `"x"` kullan; dosya varsa yazmayı reddediyor:

```python
try:
    with open("results.txt", "x", encoding="utf-8") as file:
        file.write("new line\n")
except FileExistsError:
    print("file already exists, not overwriting")
```

## 2. Dosyayı iki kez okumak

Bu, hata vermeyen ama şaşırtan bir davranış:

```python
with open("notes.txt", encoding="utf-8") as file:
    first = file.read()
    second = file.read()

print(len(first))
print(len(second))
```

```
28
0
```

İkincisi boş. Sebebi: dosyanın bir **okuma imleci** var. `read()` imleci
sonuna kadar götürüyor; ikinci `read()` sondan başlıyor ve okuyacak bir şey
bulamıyor.

Çözüm: bir kez oku, değişkende tut.

```python
with open("notes.txt", encoding="utf-8") as file:
    content = file.read()

lines = content.splitlines()
words = content.split()
```

Aynı şey `for line in file:` döngüsünden sonra da geçerli — döngü bitince
imleç sonda.

## 3. `\n` unutmak

```python
with open("names.txt", "w", encoding="utf-8") as file:
    file.write("Ada")
    file.write("Alan")
```

Dosyanın içeriği:

```
AdaAlan
```

`write` satır sonu koymuyor. `print` koyduğu için buna alışıyorsun.

```python
    file.write("Ada\n")
    file.write("Alan\n")
```

Bir liste yazacaksan tek satırda halledebilirsin:

```python
names = ["Ada", "Alan", "Grace"]

with open("names.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(names) + "\n")
```

## 4. `strip()` unutmak

```python
with open("names.txt", encoding="utf-8") as file:
    for line in file:
        if line == "Ada":
            print("found")
```

Hiçbir şey yazdırmıyor. Çünkü okunan satır `"Ada\n"`, karşılaştırdığın ise
`"Ada"`.

```python
        if line.strip() == "Ada":
```

Aynı tuzak sayıya çevirirken de var — ama orada şanslısın, `int("42\n")`
çalışıyor çünkü `int` boşlukları kendisi temizliyor. `float` da öyle. Metin
karşılaştırmasında böyle bir kolaylık yok.

## 5. `encoding` yazmamak

```python
with open("notes.txt", encoding="utf-8") as file:
```

Bunu yazmazsan Python işletim sisteminin varsayılan kodlamasını kullanıyor.
Windows'ta Türkçe bir sistemde bu genelde `cp1254`, Linux'ta `utf-8`.

Sonuç: senin bilgisayarında düzgün açılan dosya başkasınınkinde
`UnicodeDecodeError` veriyor, ya da harfler bozuk çıkıyor.

**Her `open` çağrısına yaz.** Ekstra on karakter, ömür boyu dert etmemek.

## 6. Göreli yol

```python
open("data.txt")
```

Bu dosya **programın çalıştığı klasörde** aranıyor — kod dosyasının bulunduğu
klasörde değil. İkisi farklı olabilir.

Terminalden `python scripts/main.py` çalıştırdığında Python `data.txt`
dosyasını `scripts/` içinde değil, bulunduğun klasörde arıyor.

Emin olmak istiyorsan yolu kod dosyasına göre kur:

```python
from pathlib import Path

folder = Path(__file__).parent
with open(folder / "data.txt", encoding="utf-8") as file:
    content = file.read()
```

## 7. `with` kullanmamak

```python
file = open("notes.txt", "w", encoding="utf-8")
file.write("hello")
# close cagrilmadi
```

Yazdığın şey hemen diske gitmiyor; Python bir tampon tutuyor ve dosya
kapanınca boşaltıyor. `close()` çağrılmazsa veri tamponda kalabiliyor.

Program normal biterse Python genelde temizliyor. Ama araya bir hata
girerse, ya da program uzun süre çalışacaksa, veri kaybediyorsun.

`with` bunu düşünmeyi tamamen gereksiz kılıyor.

## 8. Okumadan yazmaya geçmek

```python
with open("notes.txt", "r", encoding="utf-8") as file:
    file.write("hello")
```

```
io.UnsupportedOperation: not writable
```

Kip ne dediyse o. Okuma kipinde açılmış dosyaya yazılmıyor. Hem okuyup hem
yazman gerekiyorsa iki ayrı blok yaz — önce oku, sonra kapat, sonra yaz:

```python
with open("notes.txt", encoding="utf-8") as file:
    lines = file.read().splitlines()

lines.append("new line")

with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")
```

## Özet

| Tuzak | Sonucu |
|---|---|
| `"w"` ile açmak | Eski içerik siliniyor |
| İki kez `read()` | İkincisi boş geliyor |
| `\n` unutmak | Her şey tek satırda |
| `strip()` unutmak | Karşılaştırmalar tutmuyor |
| `encoding` yazmamak | Başka makinede bozuluyor |
| Göreli yol | Dosya bulunamıyor |
| `with` kullanmamak | Veri diske geçmeyebiliyor |
| Yanlış kip | `UnsupportedOperation` |
