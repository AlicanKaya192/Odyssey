Biçim belirteci yuvarlıyor, ama yuvarlamanın kendisi bilgisayarda
göründüğü kadar basit değil. Üç şey birbirine karışıyor.

## 1. Ondalık sayılar tam tutulmuyor

```python
print(0.1 + 0.2)
print(f"{0.1 + 0.2:.2f}")
```

```
0.30000000000000004
0.30
```

Bilgisayar ondalık sayıları ikilik tabanda saklıyor ve `0.1` oraya tam
sığmıyor. Hesap doğru, gösterim şaşırtıyor. Bu yüzden ekrana yazarken
**her zaman** biçim belirteci kullanılıyor.

Karşılaştırmada da aynı tuzak var:

```python
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
```

```
False
True
```

## 2. round() beklediğin gibi yuvarlamıyor

```python
print(round(2.5))
print(round(3.5))
```

```
2
4
```

Python yarımı en yakın **çift** sayıya yuvarlıyor. Her yarımı yukarı
yuvarlamak istiyorsan bunu kendin yazacaksın; muhasebe hesabında bu fark
önemli.

## 3. round() ile biçim belirteci farklı işler

<figure class="fig versus">
  <div class="ok">
    <h4>Biçim belirteci</h4>
    <p>Yalnızca görünüşü değiştirir. Sayı olduğu gibi kalır, sondaki sıfır
    yazılır: <code>12.50</code>.</p>
    <p>Ekrana yazdırırken, rapor üretirken kullanılır.</p>
  </div>
  <div class="dim">
    <h4>round()</h4>
    <p>Sayının kendisini değiştirir, sondaki sıfırı taşımaz:
    <code>12.5</code>.</p>
    <p>Hesap devam edecekse, sonuç bir yere kaydedilecekse kullanılır.</p>
  </div>
</figure>

## Parayla çalışırken

Kuruş önemliyse iki yol var:

1. **Kuruşu tam sayı olarak tut.** `1250` (kuruş) ile çalış, ekrana
   yazarken yüze böl. Bankacılık yazılımları böyle yapıyor.
2. **`decimal` modülünü kullan.** Ondalık sayıları tam tutuyor:

```python
from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))
```

```
0.3
```

Bu bölümde `float` yetiyor; ama parayla ilgili gerçek bir iş yazarsan
yukarıdaki iki yoldan birini seç.
