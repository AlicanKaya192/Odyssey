Listelerin üzerinde çalışan hazır metotlar var. Hepsini ezberlemene gerek yok;
en çok kullanılan altısını bilmen yeter.

## append — sona ekler

```python
teams = ["Python", "Java"]
teams.append("Go")

print(teams)     # ['Python', 'Java', 'Go']
```

Tek eleman ekler ve her zaman **sona** koyar. En sık kullanacağın metot bu.

## insert — istediğin yere ekler

```python
teams = ["Python", "Go"]
teams.insert(1, "Java")

print(teams)     # ['Python', 'Java', 'Go']
```

İlk sayı sıra numarası, ikincisi eklenecek değer. O numaradaki eleman ve
sonrasındakiler bir sağa kayar.

## remove — değere göre siler

```python
teams = ["Python", "Java", "Go"]
teams.remove("Java")

print(teams)     # ['Python', 'Go']
```

Aynı değerden birden fazla varsa **yalnızca ilkini** siler. Olmayan bir değeri
silmeye çalışırsan `ValueError` alırsın.

## pop — numaraya göre siler ve geri verir

```python
teams = ["Python", "Java", "Go"]
last = teams.pop()       # numara vermezsen sonuncuyu alir
first = teams.pop(0)

print(last)      # Go
print(first)     # Python
print(teams)     # ['Java']
```

`remove` ile farkı: `pop` sildiği elemanı **geri verir**, `remove` vermez.

## sort — sıralar

```python
numbers = [30, 10, 20]
numbers.sort()

print(numbers)     # [10, 20, 30]
```

Listeyi **yerinde** değiştirir, yeni liste üretmez. Büyükten küçüğe istersen
`numbers.sort(reverse=True)`.

Metinlerde alfabetik sıralar, ama büyük harfler küçük harflerden önce gelir —
`["b", "A"]` sıralanınca `["A", "b"]` olur.

## count ve index

```python
numbers = [10, 20, 10, 30]

print(numbers.count(10))     # 2   kac tane var
print(numbers.index(20))     # 1   ilk kacinci sirada
```

## Bir noktaya dikkat

Bu metotların çoğu listeyi **yerinde** değiştirir ve geriye `None` döner. Sık
yapılan hata şu:

```python
numbers = [30, 10, 20]
numbers = numbers.sort()     # yanlis

print(numbers)     # None
```

`sort()` listeyi zaten sıraladı; sonucunu değişkene atarsan listeyi `None` ile
ezmiş olursun. Doğrusu sadece `numbers.sort()` yazmak.
