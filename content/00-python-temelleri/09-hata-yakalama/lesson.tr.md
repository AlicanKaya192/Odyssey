# Hata Yakalama

Buraya kadar bir hata çıktığında program duruyordu. Kırmızı bir yazı, birkaç
satır dosya adı, sonra sessizlik.

Bu bazen doğru davranış. Ama her zaman değil: kullanıcı sayı yerine harf
yazdı diye programın tamamen kapanması iyi bir şey değil. "Bir sayı gir"
deyip tekrar sorması gerekirdi.

Bu bölüm o farkı öğretiyor: hangi hatayı yakalayıp devam edeceksin, hangisini
olduğu yerde bırakacaksın.

## İki tür hata

**Yazım hatası (SyntaxError)** kod daha çalışmadan çıkıyor. Python dosyayı
okurken anlamadığı bir şey görüyor:

```python
if score > 70
    print("passed")
```

```
SyntaxError: expected ':'
```

Bunu yakalayamazsın çünkü program hiç başlamıyor. Düzeltmen gerekiyor.

**Çalışma zamanı hatası** ise kod çalışırken çıkıyor. Yazımda bir sorun yok,
ama o an eldeki değerle o işlem yapılamıyor:

```python
number = int("abc")
```

```
ValueError: invalid literal for int() with base 10: 'abc'
```

Bu bölüm ikincisiyle ilgili. Bu tür hatalara **exception** deniyor.

## Traceback okumak

Hata çıktığında Python bir rapor basıyor. Uzun görünüyor ama okunması kolay:

```
Traceback (most recent call last):
  File "main.py", line 7, in <module>
    result = divide(10, 0)
  File "main.py", line 3, in divide
    return a / b
ZeroDivisionError: division by zero
```

**Aşağıdan yukarı oku.** En alt satır ne olduğunu söylüyor:
`ZeroDivisionError: division by zero`. Üstündeki satırlar oraya nasıl
gelindiğini gösteriyor — 7. satır `divide`'ı çağırmış, 3. satırda bölme
yapılmış.

Yeni başlayanların en sık hatası en üstteki satıra bakmak. Asıl bilgi
**en altta**.

## `try` / `except`

Yapı şu: riskli kodu `try` bloğuna koyuyorsun, hata çıkarsa `except` bloğu
çalışıyor.

```python
try:
    number = int("abc")
    print(number)
except ValueError:
    print("that was not a number")
```

```
that was not a number
```

Hata çıktığı anda `try` bloğunun geri kalanı **atlanıyor**. Yukarıdaki
örnekte `print(number)` hiç çalışmıyor.

Hata çıkmazsa `except` bloğu hiç çalışmıyor:

```python
try:
    number = int("42")
    print(number)
except ValueError:
    print("that was not a number")
```

```
42
```

## Hangi hatayı yakalıyorsun?

`except` yazarken hangi hatayı beklediğini söylüyorsun. Sık karşılaşacakların:

| Hata | Ne zaman çıkar |
|---|---|
| `ValueError` | Tip doğru ama değer olmaz: `int("abc")` |
| `TypeError` | Tip yanlış: `"5" + 3` |
| `ZeroDivisionError` | Sıfıra bölme |
| `KeyError` | Sözlükte olmayan anahtar |
| `IndexError` | Listede olmayan sıra numarası |
| `FileNotFoundError` | Dosya yok |
| `NameError` | Tanımlanmamış değişken |

Birden fazlasını aynı anda yakalayabilirsin:

```python
try:
    value = data[key]
except (KeyError, IndexError):
    value = None
```

Ya da her birine ayrı davranabilirsin:

```python
try:
    number = int(text)
    result = 100 / number
except ValueError:
    print("not a number")
except ZeroDivisionError:
    print("cannot divide by zero")
```

## Yapma: çıplak `except`

Böyle bir yazım var ve **her şeyi** yakalıyor:

```python
try:
    do_something()
except:            # bunu yapma
    pass
```

Sorun şu: yakaladığın şeyin ne olduğunu bilmiyorsun. Kodunda bir yazım
yanlışı varsa (`NameError`) o da bu bloğa düşüyor ve sen hiç haberdar
olmuyorsun. Program çalışıyor gibi görünüp yanlış sonuç veriyor.

Beklediğin hatayı yaz. Beklemediğin hata çıkması gerekiyor — ki fark edesin.

## Hata nesnesini almak

Hatanın kendisine ulaşmak istersen `as` kullanıyorsun:

```python
try:
    number = int("abc")
except ValueError as error:
    print("problem:", error)
```

```
problem: invalid literal for int() with base 10: 'abc'
```

`error` içinde Python'un yazdığı açıklama duruyor. Kullanıcıya göstermek için
genelde fazla teknik ama kayda geçirmek için işe yarıyor.

## `else` ve `finally`

`try`'a iki blok daha eklenebiliyor:

```python
try:
    number = int(text)
except ValueError:
    print("not a number")
else:
    print("worked:", number)
finally:
    print("done")
```

- **`else`**: hata **çıkmazsa** çalışır.
- **`finally`**: hata çıksa da çıkmasa da **her zaman** çalışır.

`finally` en çok temizlik için kullanılıyor: açılan bir dosyayı kapatmak,
bağlantıyı bırakmak gibi. Hata çıksa bile o iş yapılmalı.

## `raise` — hatayı sen çıkar

Yakalamak kadar önemli bir şey daha var: bazen hatayı **sen** çıkarmalısın.
Şimdiye kadar gördüğün hataları Python çıkarıyordu (`int("abc")` gibi).
`raise` aynısını senin kodunda yapmanı sağlıyor.

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"age cannot be negative: {age}")
    print("age saved")
    return age


print(set_age(30))
try:
    set_age(-5)
except ValueError as error:
    print("caught:", error)
```

```text
age saved
30
caught: age cannot be negative: -5
```

Ne oldu, adım adım:

- `raise ValueError("...")` bir hata kuruyor ve onu **fırlatıyor**.
  Parantezdeki metin hatanın açıklaması; `as error` ile yakalanınca
  `print` bunu yazıyor.
- `raise` çalıştığı anda fonksiyon **orada duruyor**: `-5` için
  "age saved" yazılmadı, `return` hiç çalışmadı. `return` gibi fonksiyondan
  çıkıyor; farkı, bir değer değil bir hata götürmesi.
- Hata, fonksiyonu **çağıran yere** gidiyor. Orada `try` varsa yakalanıyor;
  yoksa bir üstteki çağırana, en sonunda programın kendisine ulaşıyor ve
  program duruyor. `try` olmadan, `print(set_age(30))` satırının altına
  yalnızca `set_age(-5)` yazılsaydı traceback'in son satırında senin
  yazdığın açıklama çıkardı (dosya yolu kısaltıldı):

```text
Traceback (most recent call last):
  File "main.py", line 9, in <module>
    set_age(-5)
    ~~~~~~~^^^^
  File "main.py", line 3, in set_age
    raise ValueError(f"age cannot be negative: {age}")
ValueError: age cannot be negative: -5
```

Neden kendin hata çıkarasın? Çünkü fonksiyonun elindeki değer anlamsız ve
devam etmenin bir anlamı yok. Sessizce sıfır döndürmek yerine "bu değer
olmaz" demek, hatanın kaynağını çağıran tarafa göstermiş oluyor. Eksi bir yaş
kaydedilip üç fonksiyon sonra garip bir sonuç vermesindense, girdiği yerde
durması çok daha kolay bulunur.

**Hangi hatayı fırlatmalı?** Python'un hazır hata türlerinden durumu
anlatanı seç:

| Durum | Hata |
|---|---|
| Tür doğru ama değer olmaz (eksi yaş, boş ad) | `ValueError` |
| Tür yanlış (sayı beklenirken metin geldi) | `TypeError` |
| İstenen anahtar yok | `KeyError` |

Düz `Exception` fırlatma: çağıran onu yakalamak için `except Exception`
yazmak zorunda kalır ve böylece başka bütün hataları da yakalar. Açıklama da
neyin yanlış olduğunu ve gelen değeri söylesin: `age cannot be negative: -5`,
`invalid input`'tan çok daha yararlı.

## Yakala, bir şey yap, yeniden fırlat

Bazen hatayı yakalayıp bir not düşmek ama çözmeyi çağırana bırakmak
istersin. `except` bloğunun içinde **tek başına `raise`** yakalanan hatayı
olduğu gibi yukarı gönderir:

```python
def read_age(text):
    try:
        return int(text)
    except ValueError:
        print("could not read:", text)
        raise


try:
    read_age("abc")
except ValueError as error:
    print("caller:", error)
```

```text
could not read: abc
caller: invalid literal for int() with base 10: 'abc'
```

`read_age` hatayı gördü ve yazdı, ama yutmadı: çağıran taraf aynı hatayı
aynı açıklamayla aldı. Hatayı yakalayıp hiçbir şey yokmuş gibi devam
etmekle (`pass`) arasındaki fark bu.

Kendi hata türünü yazmak (`InsufficientFunds` gibi) sınıf bilgisi istiyor;
o, Nesne Tabanlı Programlama bölümünde.

## Ne zaman yakalanır, ne zaman bırakılır?

Basit bir ölçüt: **hatayı yakaladığında yapacak anlamlı bir şeyin var mı?**

Var ise yakala — kullanıcıdan yeniden değer iste, varsayılan bir değere
düş, mesaj göster. Yoksa bırak: hatanın görünmesi, sessizce yanlış çalışan
bir programdan iyidir.

```python
# Iyi: yapacak bir sey var
try:
    count = int(text)
except ValueError:
    count = 0

# Kotu: hata yutuldu, kimse haberdar degil
try:
    save_to_database(record)
except:
    pass
```

İkinci örnekte veri kaydedilmedi ve kimsenin haberi yok.

## Özet

- Yazım hatası kod çalışmadan çıkar, yakalanamaz; çalışma zamanı hatası
  yakalanabilir.
- Traceback **aşağıdan yukarı** okunur; ne olduğu en alt satırda yazar.
- `try` / `except` ile riskli kodu koruyorsun; hata çıkarsa `try`'ın geri
  kalanı atlanıyor.
- Hangi hatayı beklediğini yaz; çıplak `except` her şeyi yutuyor.
- `as error` ile hata açıklamasına ulaşıyorsun.
- `else` hata çıkmazsa, `finally` her durumda çalışır.
- `raise ValueError("açıklama")` hatayı sen çıkarır ve fonksiyonu orada
  durdurur; değer yanlışsa `ValueError`, tür yanlışsa `TypeError`.
- `except` içinde tek başına `raise` aynı hatayı yukarı iletir.
- Yakalayacak bir şey yapamıyorsan yakalama.
