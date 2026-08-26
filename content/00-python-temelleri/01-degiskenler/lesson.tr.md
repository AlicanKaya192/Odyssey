# Değişkenler ve Veri Tipleri

Python'da bir değeri saklamak istediğimizde **değişken** kullanırız. Değişken, içine bir şey koyduğumuz etiketli bir kutu gibi düşünülebilir.

## Değer atama

Değer atamak için `=` sembolünü kullanırız:

```python
isim = "Alican"
print(isim)
```

Metin (string) ifadeleri tırnak içine alırız. Tırnaklar çift `" "` veya tek `' '` olabilir, ikisi de aynı işi yapar:

```python
isim = "Alican"
isim = 'Alican'
```

`print()` fonksiyonu ise değişkenin içindeki değeri ekrana yazdırır.

## Sık yapılan bir hata

Tek tırnak kullanırken metnin içinde de tek tırnak geçiyorsa Python nerede bittiğini anlayamaz:

```python
hata = 'Alican'ın arabası'   # SyntaxError
```

Python `'Alican'` kısmını metin olarak görür, sonrasında gelen `ın arabası` kısmını anlamlandıramaz. Çözüm, ters eğik çizgi ile tırnağı **kaçırmaktır**:

```python
dogru = 'Alican\'ın arabası'
```

Buna Python'da **kaçış karakteri** denir. Alternatif olarak dıştaki tırnağı çift yapabilirsin: `"Alican'ın arabası"`.

## Metinlerle işlem yapmak

İki metni birleştirmek için `+` kullanırız:

```python
takim = "Beşiktaş"
takim2 = "Fenerbahçe"
print(takim + takim2)      # BeşiktaşFenerbahçe
```

Dikkat: `+` ile birleştirdiğin ifadelerin **hepsi metin olmalı**. Araya boşluk istiyorsan onu da elle eklemen gerekir:

```python
print(takim + " " + takim2)   # Beşiktaş Fenerbahçe
```

Bir metni tekrarlamak için `*` kullanılır:

```python
print(takim * 2)    # BeşiktaşBeşiktaş
```

İki metni birbiriyle çarpamazsın, hata alırsın.

## Veri tipini öğrenmek

Bir değişkenin tipini `type()` ile öğrenirsin:

```python
takim = "Beşiktaş"
yil = 1903

print(type(takim))   # <class 'str'>
print(type(yil))     # <class 'int'>
```

En sık kullanacağın temel tipler:

| Tip | Ne tutar | Örnek |
|---|---|---|
| `str` | metin | `"Beşiktaş"` |
| `int` | tam sayı | `1903` |
| `float` | ondalıklı sayı | `3.14` |
| `bool` | doğru/yanlış | `True`, `False` |

## Farklı tipleri birlikte yazdırmak

`print()` içinde virgül kullanırsan Python değerleri yan yana yazar ve aralarına kendisi boşluk koyar. Tipler farklı olsa bile sorun çıkmaz:

```python
isim = "Alican"
dogum_yili = 2001

print(isim, "doğum yılı:", dogum_yili)
# Alican doğum yılı: 2001
```

Ama `+` kullanmak istersen sayıyı önce metne çevirmen gerekir:

```python
print(str(dogum_yili) + " " + isim)   # 2001 Alican
```

Buradaki kural şu: **virgül farklı tipleri kabul eder, artı etmez.**

## Tip dönüşümü

Bir tipi başka bir tipe çevirmek için tipin adını fonksiyon gibi kullanırız:

```python
yas = "25"          # bu bir metin
yas_sayi = int(yas) # artık bir tam sayı

print(yas_sayi + 5) # 30
```

`int()`, `str()`, `float()` ve `bool()` en çok kullanacağın dönüştürücülerdir. Çevrilemeyen bir şeyi çevirmeye kalkarsan hata alırsın — örneğin `int("merhaba")` çalışmaz.

## f-string ile biçimlendirme

Metnin içine değişken yerleştirmenin en rahat yolu f-string'dir. Tırnağın önüne `f` koyar, değişkeni süslü parantez içine yazarsın:

```python
isim = "Alican"
yas = 25

print(f"{isim} {yas} yaşında.")
# Alican 25 yaşında.
```

f-string içinde işlem de yapabilirsin:

```python
print(f"5 yıl sonra {yas + 5} yaşında olacak.")
# 5 yıl sonra 30 yaşında olacak.
```

Bu yöntem `+` ile birleştirmekten hem daha okunaklı hem de tip dönüşümü derdinden kurtarır.

---

## Özet

- Değer atamak için `=` kullanılır.
- Metinler tırnak içine alınır; içeride tırnak varsa `\'` ile kaçırılır.
- `+` sadece aynı tipleri birleştirir, `,` farklı tipleri kabul eder.
- `type()` tipi söyler, `int()` / `str()` / `float()` tip çevirir.
- Metnin içine değişken koymanın en temiz yolu f-string'dir.
