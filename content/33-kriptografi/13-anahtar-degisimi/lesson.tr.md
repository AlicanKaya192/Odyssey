# Diffie-Hellman ve Eliptik Eğriler

RSA bölümünde bir simetrik anahtarı açık anahtarla şifreleyip
göndermeyi gördük. Başka bir yol daha var: iki taraf **hiç anahtar
göndermeden**, herkesin dinleyebildiği bir hat üzerinden aynı sırra
ulaşabilir. Bu fikre **anahtar değişimi** denir ve ilk yöntemi
**Diffie-Hellman**'dır. Bugün aynı fikir çoğunlukla **eliptik eğriler**
üzerinde uygulanıyor.

## Diffie-Hellman: renk karıştırma benzetmesi

Ada ve Can herkesin bildiği bir renkte anlaşır. Her biri gizli bir renk
seçer, ortak renge karıştırır ve karışımı açıkça gönderir. Sonra her biri
**karşıdan gelen karışıma kendi gizli rengini** ekler. İkisi de aynı üç
rengin karışımına ulaşır; hattı dinleyen yalnızca iki ara karışımı görür
ve karışımdan renkleri ayırmak zordur. Matematikte "karıştırmak"
`pow(g, gizli, p)`, "ayırmanın zorluğu" ise **ayrık logaritma**
problemidir (Modüler Aritmetik bölümünün tek yönlü işlemleri).

```python
p, g = 23, 5
ada_secret, can_secret = 6, 15

ada_public = pow(g, ada_secret, p)
can_public = pow(g, can_secret, p)
print(ada_public, can_public)

ada_shared = pow(can_public, ada_secret, p)
can_shared = pow(ada_public, can_secret, p)
print(ada_shared, can_shared)
```

```text
8 19
2 2
```

Açıkta giden yalnızca `p`, `g`, 8 ve 19. İki taraf da 2'ye ulaştı, çünkü
`(g ** a) ** b` ile `(g ** b) ** a` aynı sayıdır. Gizli sayılar (6 ve 15)
hiçbir zaman gönderilmedi.

## Ortak sırdan anahtara

Ortak sır doğrudan anahtar olarak kullanılmaz: bir sayıdır, uzunluğu
değişir. Anahtar Türetme bölümündeki gibi bir KDF'den geçirilir. Burada
yer kazanmak için tek bir SHA-256 kullanıyoruz; gerçekte HKDF.

```python
import hashlib

p, g = 4294967291, 5
ada_secret, can_secret = 1234567, 7654321
ada_public = pow(g, ada_secret, p)
can_public = pow(g, can_secret, p)

ada_shared = pow(can_public, ada_secret, p)
can_shared = pow(ada_public, can_secret, p)
key = hashlib.sha256(ada_shared.to_bytes(4, "big")).digest()
print(ada_shared == can_shared)
print(len(key))
print(1 < ada_public < p - 1, 1 < can_public < p - 1)
```

```text
True
32
True True
```

İki taraf aynı 32 baytlık anahtara ulaştı. Son satır bir **savunma
denetimi**: karşıdan gelen açık değer `1` ya da `p - 1` gibi bir sayıysa
ortak sır tahmin edilebilir değerlere düşer; bu yüzden gelen değer
kullanılmadan önce `1 < değer < p - 1` aralığında mı diye denetlenir.
Gerçek sistemlerde gizli sayılar `secrets` ile rastgele üretilir ve `p` en
az 2048 bittir.

## Diffie-Hellman neyi sağlamaz

Diffie-Hellman iki tarafın **aynı sırra** ulaşmasını sağlar ama karşıdaki
tarafın **kim olduğunu** doğrulamaz. Ada, Can'ın açık değeri sandığı
sayının gerçekten Can'dan geldiğini bilmezse arada biri iki tarafla ayrı
ayrı anahtar değişimi yapabilir. Bu yüzden açık değerler **imzalanır** ve
imzalayanın kimliği **sertifikayla** bağlanır: Dijital İmza ve Sertifikalar
ve PKI bölümleri bunu anlatıyor. TLS El Sıkışması bölümünde parçaların
nasıl birleştiğini göreceğiz.

İkinci önemli fikir **ileri gizlilik** (forward secrecy): her oturumda
yeni gizli sayılar üretilip iş bitince silinirse, bir gün uzun ömürlü
anahtarlar ele geçse bile eski oturumların anahtarları yeniden
hesaplanamaz.

## Eliptik eğriler

Eliptik eğri, `y² = x³ + a·x + b` denklemini sağlayan noktalardır.
Kriptografide bu denklem bir asala göre mod içinde çözülür; ortaya sonlu
sayıda nokta çıkar. Bu noktalar arasında bir **toplama** tanımlıdır: iki
noktadan geçen doğru eğriyi üçüncü bir noktada keser, onun yansıması
toplamdır. Mod içindeki formüller şöyle:

```python
P, A, B = 97, 1, 4


def on_curve(pt):
    if pt is None:
        return True
    x, y = pt
    return (y * y - (x ** 3 + A * x + B)) % P == 0


def add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        s = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P
    else:
        s = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return (x3, y3)


G = (0, 2)
print(on_curve(G))
print(add(G, G), on_curve(add(G, G)))
print(add(G, (0, 95)))
```

```text
True
(91, 48) True
None
```

`(0, 2)` eğrinin üstünde, kendisiyle toplamı da eğrinin üstünde bir nokta.
`(0, 95)` ise `(0, 2)`'nin tersi (mod 97'de `95 = -2`): toplamları
"sonsuzdaki nokta", yani toplamanın sıfırı; kodda `None`. Bölme yerine
Modüler Aritmetik bölümündeki **ters** kullanılıyor. Bu oyuncak eğride
sonsuzdaki noktayla birlikte 89 nokta var; bu sayı asal olduğu
için `G`'yi kendisiyle tekrar tekrar toplamak bütün noktaları dolaşır.

## Eliptik eğri Diffie-Hellman

Bir noktayı kendisiyle `k` kez toplamak (`k·G`) kolaydır: Modüler
Aritmetik bölümündeki kare al ve çarp fikrinin noktalar için hâli,
**ikile ve topla**. Sonuç noktadan `k`'yı bulmak ise zordur. Diffie-Hellman
aynen buraya taşınır: `pow(g, gizli, p)` yerine `gizli·G`.

```python
def mul(k, pt):
    result = None
    while k > 0:
        if k & 1:
            result = add(result, pt)
        pt = add(pt, pt)
        k >>= 1
    return result


ada_secret, can_secret = 13, 29
ada_public = mul(ada_secret, G)
can_public = mul(can_secret, G)
print(ada_public, can_public)
print(mul(ada_secret, can_public) == mul(can_secret, ada_public))
print(mul(ada_secret, can_public))
```

```text
(41, 75) (31, 12)
True
(48, 8)
```

İki taraf aynı noktaya ulaştı; o noktanın `x` koordinatı KDF'ye giren
ortak sırdır. Gerçek eğriler (X25519, P-256) 256 bitlik bir asala göre
tanımlıdır ve 2048 bitlik Diffie-Hellman'la kabaca aynı güvenliği çok daha
küçük sayılarla verir. Bu dersteki 97'lik eğri yalnızca formülleri görmek
için.

## Özet

- **Diffie-Hellman** iki tarafı, anahtar göndermeden aynı sırra ulaştırır:
  `pow(karşının_açığı, kendi_gizlim, p)`.
- Güvenlik **ayrık logaritma** probleminin zorluğuna dayanır.
- Ortak sır bir **KDF**'den geçirilip anahtar yapılır; gelen açık değer
  önce denetlenir.
- DH karşı tarafı **doğrulamaz**: açık değerler imzalanır, kimlik
  sertifikayla bağlanır.
- **Eliptik eğri DH** aynı fikri nokta toplamayla, çok daha küçük
  anahtarlarla uygular (X25519, P-256).
