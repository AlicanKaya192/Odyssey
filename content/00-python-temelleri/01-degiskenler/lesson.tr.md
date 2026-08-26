# Değişkenler ve Veri Tipleri

Python'da bir değeri saklamak istediğimizde **değişken** kullanırız. Değişken, içine bir şey koyduğumuz etiketli bir kutu gibi düşünülebilir.

## Değer atama

Değer atamak için `=` sembolünü kullanırız:

```python
name = "Alican"
print(name)
```

Metin (string) ifadeleri tırnak içine alırız. Tırnaklar çift `" "` veya tek `' '` olabilir, ikisi de aynı işi yapar:

```python
name = "Alican"
name = 'Alican'
```

`print()` fonksiyonu ise değişkenin içindeki değeri ekrana yazdırır.

## Sık yapılan bir hata

Tek tırnak kullanırken metnin içinde de tek tırnak geçiyorsa Python nerede bittiğini anlayamaz:

```python
wrong = 'Alican'ın arabası'   # SyntaxError
```

Python `'Alican'` kısmını metin olarak görür, sonrasında gelen `ın arabası` kısmını anlamlandıramaz.

> **Çözüm:** Ters eğik çizgi ile tırnağı kaçırmaktır: `'Alican\'ın arabası'`. Buna Python'da **kaçış karakteri** denir. Alternatif olarak dıştaki tırnağı çift yapabilirsin: `"Alican'ın arabası"` — bu genelde daha okunaklıdır.

## Metinlerle işlem yapmak

İki metni birleştirmek için `+` kullanırız:

```python
team = "Galatasaray"
team2 = "Trabzonspor"
print(team + team2)      # GalatasarayTrabzonspor
```

Dikkat: `+` ile birleştirdiğin ifadelerin **hepsi metin olmalı**. Araya boşluk istiyorsan onu da elle eklemen gerekir:

```python
print(team + " " + team2)   # Galatasaray Trabzonspor
```

Bir metni tekrarlamak için `*` kullanılır:

```python
print(team * 2)    # GalatasarayGalatasaray
```

İki metni birbiriyle çarpamazsın, hata alırsın.

## Veri tipini öğrenmek

Bir değişkenin tipini `type()` ile öğrenirsin:

```python
team = "Galatasaray"
year = 1903

print(type(team))   # <class 'str'>
print(type(year))   # <class 'int'>
```

En sık kullanacağın temel tipler:

| Tip | Ne tutar | Örnek |
|---|---|---|
| `str` | metin | `"Galatasaray"` |
| `int` | tam sayı | `1903` |
| `float` | ondalıklı sayı | `3.14` |
| `bool` | doğru/yanlış | `True`, `False` |

## Farklı tipleri birlikte yazdırmak

`print()` içinde virgül kullanırsan Python değerleri yan yana yazar ve aralarına kendisi boşluk koyar. Tipler farklı olsa bile sorun çıkmaz:

```python
name = "Alican"
birth_year = 2001

print(name, "doğum yılı:", birth_year)
# Alican doğum yılı: 2001
```

Ama `+` kullanmak istersen sayıyı önce metne çevirmen gerekir:

```python
print(str(birth_year) + " " + name)   # 2001 Alican
```

Buradaki kural şu: **virgül farklı tipleri kabul eder, artı etmez.**

## Tip dönüşümü

Bir tipi başka bir tipe çevirmek için tipin adını fonksiyon gibi kullanırız:

```python
age = "25"          # bu bir metin
age_number = int(age) # artık bir tam sayı

print(age_number + 5) # 30
```

`int()`, `str()`, `float()` ve `bool()` en çok kullanacağın dönüştürücülerdir. Çevrilemeyen bir şeyi çevirmeye kalkarsan hata alırsın — örneğin `int("merhaba")` çalışmaz.

## f-string ile biçimlendirme

Metnin içine değişken yerleştirmenin en rahat yolu f-string'dir. Tırnağın önüne `f` koyar, değişkeni süslü parantez içine yazarsın:

```python
name = "Alican"
age = 25

print(f"{name} {age} yaşında.")
# Alican 25 yaşında.
```

f-string içinde işlem de yapabilirsin:

```python
print(f"5 yıl sonra {age + 5} yaşında olacak.")
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
