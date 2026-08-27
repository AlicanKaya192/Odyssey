# Koşul Durumları

Şimdiye kadar yazdığın kod hep baştan sona, aynı sırayla çalıştı. Koşullar bunu değiştirir: programın duruma göre farklı yollar izlemesini sağlar.

## if

En basit hâli: bir koşul doğruysa bir şey yap.

```python
age = 20

if age >= 18:
    print("Oy kullanabilirsin.")
```

`if` satırı iki nokta üst üste ile biter, altındaki blok girintili yazılır. Koşul yanlışsa o blok hiç çalışmaz ve program devam eder.

## else

Koşul yanlış olduğunda başka bir şey yapmak istiyorsan:

```python
age = 15

if age >= 18:
    print("Oy kullanabilirsin.")
else:
    print("Henüz oy kullanamazsın.")
```

`else` bir koşul almaz — "yukarıdakilerin hiçbiri değilse" anlamına gelir.

## elif

İkiden fazla ihtimal varsa `elif` kullanılır. Not harfi hesaplamak buna iyi bir örnek:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)   # B
```

Burada dikkat edilmesi gereken şey **sıra**. Python koşulları yukarıdan aşağıya dener ve **ilk doğru olanı çalıştırıp geri kalanına hiç bakmaz.**

Bu yüzden `score = 95` olsaydı sadece ilk satır çalışır, `score >= 80` hiç denenmezdi. Koşulları yanlış sırayla yazarsan sorun çıkar:

```python
# YANLIŞ SIRA
if score >= 70:
    grade = "C"
elif score >= 90:
    grade = "A"    # buraya hiç ulaşılmaz
```

95 puan alan biri bile "C" alır, çünkü ilk koşul zaten doğrudur. Kural şu: **dar koşuldan geniş koşula doğru yaz.**

## Koşulları birleştirmek

Bir önceki bölümde öğrendiğin `and`, `or` ve `not` burada işe yarar:

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("Girebilirsin.")
```

`and` ikisinin de doğru olmasını ister, `or` birinin yeterli olduğunu söyler.

## İç içe koşullar

Bir `if` bloğunun içine başka bir `if` yazabilirsin:

```python
age = 25
has_ticket = False

if age >= 18:
    if has_ticket:
        print("Girebilirsin.")
    else:
        print("Bilet almalısın.")
else:
    print("Yaşın yetmiyor.")
```

İşe yarar ama fazla iç içe geçerse kod okunmaz hâle gelir. Üç seviyeden fazla iç içe `if` gördüğünde genelde daha iyi bir yazım vardır.

## Doğruluk değerleri

Python'da sadece `True` ve `False` değil, başka değerler de koşul olarak kullanılabilir. Boş şeyler yanlış sayılır:

```python
name = ""

if name:
    print("Merhaba", name)
else:
    print("İsim boş.")
```

Boş metin, sıfır ve boş liste **yanlış** sayılır; dolu olanlar doğru. Bu kısayol koda alışkınlık geldiğinde işini kolaylaştırır.

---

## Özet

- `if` koşul doğruysa çalışır, gövdesi girintili yazılır.
- `else` "hiçbiri değilse" demektir, koşul almaz.
- `elif` ikiden fazla ihtimal için kullanılır.
- Python **ilk doğru koşulu** çalıştırır, geri kalanına bakmaz — sıra önemlidir.
- `and`, `or` ve `not` ile birden fazla koşul birleştirilir.
