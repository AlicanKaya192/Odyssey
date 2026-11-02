# XOR ve Tek Kullanımlık Şifre

Klasik Şifreleri Kırmak bölümü bir hedefle bitti: şifreli metin, anahtarı
bilmeyen biri için rastgeleden ayırt edilemesin. Bu hedefe **kesin olarak**
ulaşan bir yöntem var: **tek kullanımlık şifre** (one-time pad, OTP). Hem de
matematiksel olarak kanıtlanmış biçimde. Ama yalnızca dört koşulun hepsine
uyulursa. Bu bölüm o yöntemi, temelindeki **XOR** işlemini ve koşullardan
biri çiğnenince neler olduğunu anlatıyor.

## XOR

**XOR** (dışlayıcı veya, exclusive or) iki biti karşılaştırır: farklıysa
1, aynıysa 0. Python'da işareti `^`. Sayılarda her bit ayrı ayrı XOR'lanır:

| a | b | a ^ b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

```python
a, b = 0b1100, 0b1010
print(f"{a:04b} ^ {b:04b} = {a ^ b:04b}")
print(a ^ b ^ b == a, a ^ a, a ^ 0)
```

```text
1100 ^ 1010 = 0110
True 0 12
```

İkinci satırdaki üç özellik bu bölümün tamamını taşıyor:

- `a ^ b ^ b == a`: aynı değerle iki kez XOR'lamak geri getirir. Şifreleme
  ile çözme **aynı işlemdir**.
- `a ^ a == 0`: bir şey kendisiyle XOR'lanınca yok olur.
- `a ^ 0 == a`: sıfırla XOR hiçbir şeyi değiştirmez.

## Tek kullanımlık şifre

Mesajın her baytı, anahtarın aynı sıradaki baytıyla XOR'lanır. Anahtar
mesaj kadar uzun ve tamamen rastgeledir:

```python
def xor_bytes(data, key):
    return bytes(d ^ k for d, k in zip(data, key))


message = b"PAY BOB 100"
key = bytes.fromhex("3a91c47e0b5d22f6a8137e")
cipher = xor_bytes(message, key)
print(cipher.hex())
print(xor_bytes(cipher, key))
```

```text
6ad09d5e491260d699234e
b'PAY BOB 100'
```

Örnekte anahtarı sabit yazdık ki çıktı her çalıştırmada aynı olsun.
Gerçekte anahtar `secrets.token_bytes(len(message))` ile üretilir
(Rastgelelik bölümü). `bytes.hex()` baytları onaltılık metne, `bytes.fromhex`
geri çevirir.

## Neden kırılamaz?

Klasik şifreleri kırarken her seferinde "bu çözüm anlamlı mı?" diye
sorduk. Tek kullanımlık şifrede bu soru işe yaramaz, çünkü aynı şifreli
metin, uygun bir anahtarla **aynı uzunluktaki her mesaja** çözülebilir:

```python
other = b"PAY EVE 900"
fake_key = xor_bytes(cipher, other)
print(xor_bytes(cipher, fake_key))
```

```text
b'PAY EVE 900'
```

Saldırgan bütün anahtarları denese bile `PAY BOB 100`'ü de, `PAY EVE 900`'ü
de, aynı uzunluktaki her cümleyi de bulur ve hangisinin doğru olduğunu
bilemez. Bilgi kuramının kurucusu Shannon 1949'da bunu kanıtladı ve **mükemmel gizlilik**
(perfect secrecy) adını verdi: şifreli metin, mesaj hakkında **uzunluğu
dışında** hiçbir şey söylemez.

## Dört koşul

Kanıt yalnızca şu koşulların hepsi tutarsa geçerlidir:

1. Anahtar **gerçekten rastgele** olmalı.
2. Anahtar en az **mesaj kadar uzun** olmalı.
3. Anahtar **yalnızca bir kez** kullanılmalı.
4. Anahtar **gizli** kalmalı.

Bu koşullar tek kullanımlık şifreyi pratikte neredeyse kullanılmaz kılar:
1 GB veri göndermek için önce 1 GB anahtarı karşı tarafa güvenle
ulaştırmak gerekir. O anahtarı güvenle ulaştırabiliyorsan, mesajı da aynı
yoldan gönderebilirdin. Yine de modern **akış şifreleri** (stream cipher)
aynı fikri kullanır: kısa bir anahtardan uzun, rastgele görünen bir dizi
üretip mesajla XOR'lar. Simetrik Şifreleme bölümünde göreceğiz.

## Koşul 3 çiğnenirse: anahtarı tekrar kullanmak

İki mesaj aynı anahtarla şifrelenirse, iki şifreli metni XOR'lamak anahtarı
**yok eder** (`k ^ k = 0`) ve geriye iki mesajın XOR'u kalır:

```python
m1 = b"ATTACK AT DAWN"
m2 = b"RETREAT AT TEN"
key = bytes.fromhex("5f0e2b9ac4d17733e1a6082cb94d")
c1 = xor_bytes(m1, key)
c2 = xor_bytes(m2, key)

leak = xor_bytes(c1, c2)
print(leak == xor_bytes(m1, m2))
print(xor_bytes(leak, m1))
```

```text
True
b'RETREAT AT TEN'
```

Saldırgan anahtarı hiç görmedi. Yine de birinci mesajı bildiği (ya da
tahmin ettiği) anda ikincisini okudu. Birinci mesajı bilmese bile iki
düz metnin XOR'u, Klasik Şifreleri Kırmak bölümündeki istatistik
yöntemleriyle çözülebilecek kadar iz taşır. 1940'larda bir devletin
tek kullanımlık şifre sayfalarını yeniden kullanması, karşı tarafın
binlerce mesajı yıllar sonra okumasına yol açtı.

Bu hata bugün de yaşanıyor: akış şifrelerinde aynı anahtar ve aynı
başlangıç değeri (nonce) iki kez kullanılınca tam olarak bu olur (Sık
Kriptografi Hataları bölümü).

## Gizlilik bütünlük değildir

Tek kullanımlık şifre mesajı gizler ama **değiştirilmesini engellemez**.
Saldırgan mesajın biçimini biliyorsa, anahtarı bilmeden şifreli metni
istediği gibi değiştirebilir. Bir bit çevrilince düz metinde de aynı bit
çevrilir:

```python
cipher = xor_bytes(b"PAY BOB 100", key)
patch = xor_bytes(b"PAY BOB 100", b"PAY BOB 900")
tampered = xor_bytes(cipher, patch)
print(xor_bytes(tampered, key))
```

```text
b'PAY BOB 900'
```

Saldırgan yalnızca "bu mesaj `PAY BOB 100`" bilgisini kullandı; anahtarı
hiç görmedi ve alıcı 900 ödemesi gören, kusursuz çözülen bir mesaj aldı.
Buna **değiştirilebilirlik** (malleability) denir. Çözüm şifrelemenin
yanına bir bütünlük denetimi koymaktır: HMAC (Mesaj Doğrulama: HMAC
bölümü) ya da ikisini
birlikte yapan doğrulanmış şifreleme (Doğrulanmış Şifreleme bölümü).
Kriptografi Nedir? bölümündeki tabloyu hatırla: gizlilik ve bütünlük ayrı
amaçlardır, ayrı araç ister.

## Özet

- **XOR** farklı bitlerde 1 verir; `a ^ b ^ b == a`, bu yüzden şifreleme ve
  çözme aynı işlemdir.
- **Tek kullanımlık şifre:** mesaj, mesaj kadar uzun rastgele bir anahtarla
  XOR'lanır. Shannon'a göre **mükemmel gizlilik** sağlar: aynı şifreli metin
  aynı uzunluktaki her mesaja çözülebilir.
- Dört koşul: gerçekten rastgele, mesaj kadar uzun, **tek kullanımlık**,
  gizli. Pratikte anahtarı taşımak mesajı taşımak kadar zordur.
- Anahtar tekrar kullanılırsa `c1 ^ c2 = m1 ^ m2`: anahtarsız sızıntı.
- Şifreleme bütünlük sağlamaz: XOR'lanmış metin bit bit değiştirilebilir.
