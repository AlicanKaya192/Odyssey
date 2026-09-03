Hata çıktığında ekrana basılan o uzun yazının adı **traceback**. Korkutucu
görünüyor ama düzenli bir yapısı var ve okuması öğrenilince hatanın yerini
saniyeler içinde buluyorsun.

## Yapısı

```
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    report = build_report(users)
  File "main.py", line 7, in build_report
    return summarize(data)
  File "main.py", line 3, in summarize
    return total / count
ZeroDivisionError: division by zero
```

Üç parçadan oluşuyor:

1. **İlk satır** her zaman aynı: "en son çağrı en altta".
2. **Ortadaki satırlar** çağrı zinciri. Her ikili bir satırı gösteriyor:
   hangi dosya, kaçıncı satır, hangi fonksiyon — ve altında o satırın kendisi.
3. **Son satır** asıl hata: türü ve açıklaması.

## Aşağıdan yukarı oku

En alt satır ne olduğunu söylüyor. Onun hemen üstündeki satır ise **hatanın
gerçekten çıktığı yer**.

Yukarıdaki örnekte:

- Ne oldu? Sıfıra bölme.
- Nerede? `main.py` 3. satır, `summarize` fonksiyonunun içinde.
- Oraya nasıl gelindi? 12. satır `build_report`'u çağırmış, o da 7. satırda
  `summarize`'ı çağırmış.

İlk bakılacak yer **sondan ikinci** satır grubu. Yukarıdakiler yalnızca yolu
gösteriyor.

## Senin kodun hangisi?

Bazen zincirde kütüphane dosyaları da görünüyor:

```
  File "C:\Python314\Lib\json\decoder.py", line 355, in raw_decode
```

Bunlar genelde suçlu değil. **Kendi dosyanın adının geçtiği en alttaki
satıra bak** — hata çoğunlukla oraya verdiğin bir değerden çıkıyor.

## Hata satırı yanıltabilir

Python hatayı bazen bir sonraki satırda gösteriyor. Kapatılmamış bir parantez
buna en iyi örnek:

```python
print("total:", total
print("done")
```

```
  File "main.py", line 2
    print("done")
    ^^^^^
SyntaxError: invalid syntax
```

Hata 2. satırda gösteriliyor ama sorun 1. satırdaki açık parantez. Python ilk
satırın devam ettiğini sanıyor ve ikinci satırda pes ediyor.

**Kural: gösterilen satırda bir şey bulamıyorsan bir üstüne bak.**

## Kendi hatanı okunur kılmak

`raise` ile hata çıkarırken yazdığın açıklama traceback'in son satırında
görünüyor. Onu iyi yazmak sonradan sana zaman kazandırıyor:

```python
raise ValueError("age cannot be negative")
```

```
ValueError: age cannot be negative
```

Kötü örnek:

```python
raise ValueError("error")
```

Bu satırı üç ay sonra gördüğünde hangi değerin sorun çıkardığını
bilemeyeceksin. Mümkünse değeri de yaz:

```python
raise ValueError(f"age cannot be negative: {age}")
```

## Uygulamanın içindeki hatalar

Bu uygulamada alıştırma kodun ayrı bir süreçte çalışıyor ve hata çıkarsa
traceback sana sadeleştirilmiş hâliyle gösteriliyor: uygulamanın kendi
dosyaları ayıklanıyor, senin kodunun satırı öne çıkarılıyor.

Yani ekranda gördüğün satır numarası **senin yazdığın kodun** satır numarası.
Kendi bilgisayarında bir dosya çalıştırdığında ise yukarıdaki tam hâlini
göreceksin.
