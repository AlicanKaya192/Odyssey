# Klasik Şifreler

Bilgisayarlardan çok önce de insanlar mesajlarını gizlemek istedi. Bu
bölümdeki **klasik şifreler** (classical ciphers) harflerle elle yapılır ve
bugün hiçbiri güvenli değil. Yine de öğrenmeye değerler: modern
kriptografinin iki temel hareketi, **yer değiştirme** (substitution) ve
**yer karıştırma** (transposition), ilk kez burada görünür; neden
kırıldıklarını görmek de neden bugünkü algoritmalara ihtiyaç duyulduğunu
anlatır. Bir sonraki bölüm, Klasik Şifreleri Kırmak, bunların hepsini
kıracak.

## Sezar şifresi

Julius Caesar'ın kullandığı söylenen en basit şifre: her harf alfabede
sabit bir sayı kadar **kaydırılır**. Kaydırma 3 ise `A` → `D`, `B` → `E`,
`Z` → `C` olur (sona gelince başa döner). Anahtar kaydırma sayısıdır.

Kaydırmayı harfin alfabedeki sırası üzerinden `% 26` ile yaparız; harf
olmayanlara dokunmayız:

```python
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


secret = caesar("Attack at dawn!", 3)
print(secret)
print(caesar(secret, -3))
print(caesar("Hello", 13), caesar(caesar("Hello", 13), 13))
```

```text
Dwwdfn dw gdzq!
Attack at dawn!
Uryyb Hello
```

Çözmek, ters yönde kaydırmaktır (`-3`). Son satırdaki **ROT13** özel bir
durum: 26 harfin tam yarısı kadar kaydırdığı için iki kez uygulayınca
başa dönülür, şifreleme ve çözme aynı işlemdir. ROT13 bugün yalnızca
"bulmacanın cevabını hemen görme" gibi şakalarda kullanılır; Kriptografi
Nedir? bölümündeki Base64 gibi, gizlilik sağlamaz.

Sezar şifresinin zayıflığı açık: yalnızca **26 anahtar** var (0 dahil).
Kaba kuvvetle hepsini denemek bir saniye bile sürmez.

## Yerine koyma şifresi

Anahtar sayısını büyütmek için harfleri sabit bir sayıyla kaydırmak yerine
her harfe karşılık **rastgele** bir harf seçebiliriz. Anahtar bu durumda
26 harfin bir sıralamasıdır:

```python
import math
import string

plain = string.ascii_lowercase
key = "qwertyuiopasdfghjklzxcvbnm"
table = str.maketrans(plain, key)
back = str.maketrans(key, plain)

secret = "attack at dawn".translate(table)
print(secret)
print(secret.translate(back))
keys = math.factorial(26)
print(f"{keys:.2e} keys, {math.log2(keys):.1f} bits")
```

```text
qzzqea qz rqvf
attack at dawn
4.03e+26 keys, 88.4 bits
```

Yaklaşık 88 bitlik bir anahtar uzayı: Kriptografi Nedir? bölümündeki
hesaba göre kaba kuvvetle denemek milyonlarca yıl sürer. Yine de bu şifre
birkaç dakikada kırılır, çünkü kaba kuvvete gerek yoktur: aynı harf **hep
aynı harfe** dönüşür ve dilin harf sıklıkları şifreli metinde olduğu gibi
kalır. Ders şu: **büyük anahtar uzayı tek başına güvenlik değildir.**
Bir sonraki bölümde bunu ölçerek göreceğiz.

**Atbash** bu ailenin en eski üyelerinden: alfabe ters çevrilir (`a` ↔
`z`, `b` ↔ `y`). Anahtarı yoktur; Sezar'dan da zayıftır.

## Vigenère şifresi

16. yüzyılda yaygınlaşan **Vigenère** (Vijener okunur), harf sıklığı
sorununa bir cevaptır: tek bir kaydırma yerine bir **anahtar kelimenin**
harfleri sırayla kaydırma olarak kullanılır. Anahtar `lemon` ise birinci
harf `l` (11) kadar, ikincisi `e` (4) kadar kaydırılır ve anahtar bitince
başa dönülür. Böylece aynı düz metin harfi farklı yerlerde farklı harflere
dönüşür.

```python
def vigenere(text, key, sign=1):
    result = ""
    i = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key[i % len(key)].lower()) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + sign * shift) % 26 + base)
            i += 1
        else:
            result += ch
    return result


secret = vigenere("attack at dawn", "lemon")
print(secret)
print(vigenere(secret, "lemon", -1))
```

```text
lxfopv ef rnhr
attack at dawn
```

Dikkat: anahtarın sırası (`i`) yalnızca **harflerde** ilerliyor; boşluk
anahtar harfi harcamıyor. İlk satırdaki iki `a` harfinin (`attack`'in ilk
ve dördüncü harfi) birinin `l`, öbürünün `o` olduğuna bak.

Vigenère üç yüz yıl kırılamaz sanıldı ve "çözülemez şifre" diye anıldı.
Zayıflığı anahtarın **tekrar etmesidir**: anahtar uzunluğu bilinince metin
anahtar harfi başına ayrı Sezar şifrelerine bölünür ve her biri ayrı
kırılır. Bunun yolunu bir sonraki bölümde göreceğiz.

## Yer karıştırma şifreleri

Şimdiye kadarki şifreler harfleri **değiştirdi**. **Yer karıştırma**
(transposition) şifreleri harflere dokunmaz, yalnızca **sıralarını**
değiştirir. En basiti **çit şifresi** (rail fence): harfler bir zikzak
hâlinde birkaç satıra yazılır, sonra satırlar art arda okunur.

```python
def rail_fence(text, rails):
    if rails == 1:
        return text
    rows = [""] * rails
    row, step = 0, 1
    for ch in text:
        rows[row] += ch
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    return "".join(rows)


print(rail_fence("WEAREDISCOVERED", 3))
print(rail_fence("WEAREDISCOVERED", 1))
```

```text
WECRERDSOEEAIVD
WEAREDISCOVERED
```

Şifreli metinde harf sıklıkları **hiç değişmez**: ne kadar `E` varsa yine
o kadar `E` var. Bu yüzden harf sayımı yer karıştırmayı hemen ele verir;
anahtar uzayı da küçüktür (satır sayısı).

## İki temel hareket

<figure class="fig"><div class="versus">
  <div><h4>Yer değiştirme (substitution)</h4>Her harf başka bir harfe dönüşür: Sezar, yerine koyma, Vigenère. Modern şifrelerdeki <b>karışıklık</b> (confusion) fikrinin atası.</div>
  <div><h4>Yer karıştırma (transposition)</h4>Harfler aynı kalır, yerleri değişir: çit şifresi. Modern şifrelerdeki <b>yayılma</b> (diffusion) fikrinin atası.</div>
</div><figcaption>Modern blok şifreleri ikisini birçok tur boyunca üst üste uygular.</figcaption></figure>

Tek başına ikisi de zayıftır. Modern şifreler (Simetrik Şifreleme
bölümündeki AES gibi) ikisini bilgisayarla birçok tur boyunca birlikte
uygular; böylece ne harf sıklığı ne de sıra düz metinden şifreli metne
taşınır.

## Özet

- **Sezar:** sabit kaydırma, 26 anahtar; **ROT13** kendi tersidir.
- **Yerine koyma:** 26! (≈ 88 bit) anahtar, ama aynı harf hep aynı harfe
  döndüğü için harf sıklığıyla kırılır. Büyük anahtar uzayı tek başına
  güvenlik değildir.
- **Vigenère:** anahtar kelimeyle değişen kaydırma; zayıflığı anahtarın
  tekrar etmesi.
- **Yer karıştırma:** harfler aynı, sıra değişir; harf sıklığı olduğu gibi
  kalır.
- Yer değiştirme ve yer karıştırma, modern şifrelerdeki karışıklık ve
  yayılmanın atalarıdır.
