# RSA

Modüler Aritmetik bölümü bir yönde kolay, öteki yönde zor işlemlerle
bitti: iki asalı çarpmak kolay, çarpımı asallarına ayırmak zor. **RSA**
bu farkı bir **anahtar çiftine** çevirir: herkese verilen bir **açık
anahtar** ve yalnızca sahibinde kalan bir **özel anahtar**. Açık anahtarla
şifrelenen mesajı yalnızca özel anahtar çözer. Bu bölümde küçük, oyuncak
sayılarla RSA'yı adım adım kuruyoruz.

## Anahtar çiftini kurmak

1. İki asal seç: `p`, `q`.
2. Modül: `n = p * q`. Açık anahtarın parçası.
3. `phi = (p - 1) * (q - 1)`. Gizli kalır.
4. Açık üs `e`: `phi` ile ortak böleni 1 olan bir sayı (genelde 65537).
5. Özel üs `d`: `e`'nin mod `phi`'deki tersi.

```python
import math

p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
print(n, phi)
print(math.gcd(e, phi))
d = pow(e, -1, phi)
print(d)
print(e * d % phi)
```

```text
3233 3120
1
2753
1
```

Açık anahtar `(e, n) = (17, 3233)`, özel anahtar `(d, n) = (2753, 3233)`.
`d`, Modüler Aritmetik bölümündeki ters: `e * d % phi == 1`. `phi`'yi
hesaplamak için `p` ile `q`'yu bilmek gerekir; `n`'i bilen ama asallarını
bilmeyen biri `d`'yi bulamaz.

## Şifrelemek ve çözmek

Mesaj `n`'den küçük bir sayı olmalı. Şifreleme `c = m ** e mod n`, çözme
`m = c ** d mod n`.

```python
m = 65
c = pow(m, e, n)
print(c)
print(pow(c, d, n))
```

```text
2790
65
```

65 şifrelenince 2790 oldu, 2790 çözülünce 65 geri geldi. Bunun neden işe
yaradığını Fermat'nın küçük teoreminin genelleştirilmiş hâli (Euler
teoremi) açıklar: `e * d`, `phi`'nin bir
katından 1 fazla olduğu için `m ** (e * d) mod n`, `m`'in kendisine döner.

## Metni sayıya çevirmek

RSA sayılarla çalışır; metin önce bayta, bayt da sayıya çevrilir. Sayı
`n`'den küçük olmalı, o yüzden bu örnekte biraz daha büyük oyuncak asallar
kullanıyoruz.

```python
p, q = 104723, 104729
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

m = int.from_bytes(b"hi!", "big")
print(m, m < n)
c = pow(m, e, n)
back = pow(c, d, n)
print(back.to_bytes(3, "big"))
```

```text
6842657 True
b'hi!'
```

`int.from_bytes` baytları tek bir sayıya çevirdi, şifre çözüldükten sonra
`to_bytes` geri çevirdi. Gerçek RSA'da `n` 2048 bit ya da daha büyüktür;
bizim `n` yalnızca 34 bit ve bu kadar küçük bir sayı kolayca asallarına
ayrılır. Oyuncak sayılar yalnızca adımları görmek için.

## Ders kitabı RSA'sı neden yetmez

Buraya kadarki "ders kitabı" RSA'sının bir özelliği güvenlik sorunu
yaratır: **aynı mesaj her zaman aynı şifreli metni verir.**

```python
c1 = pow(int.from_bytes(b"yes", "big"), e, n)
c2 = pow(int.from_bytes(b"yes", "big"), e, n)
c3 = pow(int.from_bytes(b"no", "big"), e, n)
print(c1 == c2)
print(c1 == c3)
```

```text
True
False
```

Açık anahtar herkeste olduğu için, olası cevaplar az olduğunda ("yes",
"no") herkes her birini kendisi şifreleyip şifreli metinle
karşılaştırabilir. Blok Şifre Kipleri bölümündeki ECB sorununun açık
anahtardaki hâli bu. Gerçek RSA bu yüzden şifrelemeden önce mesaja
**rastgele dolgu** ekler: bugünkü standart **OAEP**. Dolgu aynı mesajın
her seferinde farklı bir şifreli metin vermesini sağlar.

## RSA gerçekte nerede

RSA yavaştır ve yalnızca `n`'den küçük bir mesajı şifreleyebilir. Bu yüzden
büyük veriyi doğrudan şifrelemek için kullanılmaz:

<figure class="fig">
<div class="flow">
<span class="node">Rastgele simetrik anahtar</span>
<span class="arrow">→</span>
<span class="node acc">RSA ile şifrelenir</span>
<span class="arrow">→</span>
<span class="node">Veri AES-GCM ile</span>
<span class="arrow">→</span>
<span class="node ok">Alıcı anahtarı çözer</span>
</div>
<figcaption>Karma şifreleme: RSA yalnızca kısa simetrik anahtarı taşır, veriyi doğrulanmış şifreleme şifreler.</figcaption>
</figure>

RSA'nın ikinci kullanımı **dijital imza**: özel anahtarla imzalanan bir
mesajı herkes açık anahtarla doğrulayabilir. Bunu Dijital İmza bölümü
anlatıyor. Bugün anahtar değişiminde ise çoğunlukla Diffie-Hellman ve
eliptik eğriler kullanılıyor (sonraki bölüm).

## Özet

- RSA'da **açık anahtar** `(e, n)` herkese verilir, **özel anahtar**
  `(d, n)` sahibinde kalır.
- `n = p * q`; `d`, `e`'nin mod `(p - 1)(q - 1)`'deki tersidir.
- Şifreleme `pow(m, e, n)`, çözme `pow(c, d, n)`; mesaj `n`'den küçük olmalı.
- Güvenlik, büyük `n`'i asallarına ayırmanın zorluğuna dayanır; gerçek `n`
  en az 2048 bit.
- Ders kitabı RSA'sı belirleyicidir; gerçekte **OAEP** dolgusu ve karma
  şifreleme kullanılır.
