# Modüler Aritmetik

Buraya kadarki bütün araçlar **simetrikti**: iki taraf aynı anahtarı
paylaşıyordu. Ama o anahtar ilk kez nasıl paylaşılır? Hiç tanışmamış iki
bilgisayar, herkesin dinleyebildiği bir hat üzerinden ortak bir sırra nasıl
ulaşır? Sonraki bölümlerin cevabı (RSA, Diffie-Hellman) tek bir matematik
alanına dayanıyor: **modüler aritmetik**. Bu bölüm o araç kutusunu kuruyor.

## Saat aritmetiği

Saat 10'dan 5 saat sonrası 15 değil, 3'tür: 12'ye ulaşınca başa
dönülür. Bu "başa dönen" aritmetiğe **mod** denir. `a mod n`, `a`'nın
`n`'e bölümünden kalandır; Python'da `%`.

```python
print((10 + 5) % 12)
print(27 % 12)
print((-3) % 12)
print((7 * 8) % 12)
```

```text
3
3
9
8
```

Python'da sonuç her zaman `0` ile `n - 1` arasındadır, eksi sayıda bile:
saat 0'dan 3 saat geri 9'dur. Toplama ve çarpma mod içinde olduğu gibi
çalışır; istersen her adımda `% n` alabilirsin, sonuç değişmez.

## Büyük üsler: `pow(taban, üs, mod)`

Kriptografide `taban ** üs % mod` biçiminde, yüzlerce basamaklı sayılarla
hesap yapılır. Önce üssü hesaplayıp sonra kalanı almak gereksiz büyük
sayılar üretir; `pow`'un üç argümanlı hâli ara sonuçları hep mod içinde
tutar.

```python
print(len(str(7 ** 128)))
print(7 ** 128 % 13)
print(pow(7, 128, 13))
```

```text
109
3
3
```

İki yol aynı sonucu verdi ama birincisi 109 basamaklı bir sayı kurdu.
Gerçek üsler yüzlerce basamaklı olduğunda bu yol hiç bitmez. `pow`'un
kullandığı fikir **kare al ve çarp**: üssün ikili basamaklarına bakılır,
her adımda taban karesi alınır, basamak 1 ise sonuçla çarpılır.

```python
def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


print(mod_pow(7, 128, 13))
print(mod_pow(5, 117, 19) == pow(5, 117, 19))
print(bin(117))
```

```text
3
True
0b1110101
```

117'nin ikili yazımı yedi basamak: döngü yalnızca yedi tur döndü. Üs bin
basamaklı bile olsa tur sayısı basamak sayısı kadardır; bu yüzden
kriptografideki dev üsler hızla hesaplanır.

## En büyük ortak bölen ve ters

Mod içinde bölme yoktur; yerine **ters** vardır. `a`'nın mod `n`'deki
tersi, `a * x % n == 1` olan `x` sayısıdır. Ters ancak `a` ile `n`'in
**en büyük ortak böleni** (ebob, gcd) 1 ise vardır.

```python
import math

print(math.gcd(12, 18))
print(math.gcd(3, 11))
inverse = pow(3, -1, 11)
print(inverse, 3 * inverse % 11)
try:
    pow(4, -1, 8)
except ValueError as error:
    print("no inverse:", error)
```

```text
6
1
4 1
no inverse: base is not invertible for the given modulus
```

3'ün mod 11'deki tersi 4: `3 × 4 = 12`, 11'e bölününce kalan 1. 4 ile 8'in
ortak böleni 2 olduğu için 4'ün mod 8'de tersi yok ve Python bunu hatayla
söylüyor.

Tersi bulmanın klasik yolu **genişletilmiş Öklid algoritması**:
`a * x + b * y == gcd(a, b)` eşitliğini sağlayan `x` ve `y`'yi de bulur.
Ebob 1 ise `x` tam olarak `a`'nın tersidir.

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


g, x, y = egcd(3, 11)
print(g, x, y)
print(3 * x + 11 * y)
print(x % 11)
```

```text
1 4 -1
1
4
```

`3 × 4 + 11 × (-1) = 1`: `x = 4` tersin kendisi. `x` bazen eksi çıkar;
`x % 11` onu `0` ile `10` arasına getirir. RSA bölümünde gizli anahtar tam
olarak böyle, bir sayının tersi olarak bulunacak.

## Fermat'nın küçük teoremi

`p` asal ise ve `a`, `p`'ye bölünmüyorsa `a ** (p - 1) % p` her zaman 1'dir.
Bu, asal sayılarla mod alınca ortaya çıkan düzenin ilk işareti.

```python
print([pow(a, 6, 7) for a in range(1, 7)])
print([pow(a, 7, 8) for a in range(1, 8)])
```

```text
[1, 1, 1, 1, 1, 1]
[1, 0, 3, 0, 5, 0, 7]
```

7 asal: bütün sonuçlar 1. 8 asal değil: sonuçlar 1 değil. RSA'nın şifre
çözmesinin neden işe yaradığını bu teorem açıklıyor; asal sayılar bu
yüzden açık anahtarlı kriptografinin merkezinde.

## Özet

- `a % n` bölümden kalandır; Python'da sonuç hep `0` ile `n - 1` arasında.
- `pow(taban, üs, mod)` büyük üsleri **kare al ve çarp** ile, üssün basamak
  sayısı kadar adımda hesaplar.
- Mod içinde bölme yerine **ters** vardır; yalnızca ebob 1 ise bulunur:
  `pow(a, -1, n)`.
- **Genişletilmiş Öklid** tersi adım adım bulur.
- `p` asalsa `a ** (p - 1) % p == 1` (Fermat); RSA buna dayanır.
