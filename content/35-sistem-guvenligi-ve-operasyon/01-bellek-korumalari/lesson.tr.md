# Bellek Korumaları: ASLR, DEP, Canary

Bellek Güvenliği ve Arabellek Taşması bölümünde bir taşmanın komşu veriyi
sessizce bozduğunu gördük. En iyi çözüm bu hataları hiç yazmamaktır: bellek
güvenli bir dil seçmek, yazmadan önce ölçmek. Ama dünyada milyonlarca satır
C ve C++ kodu çalışıyor ve hepsi bir günde düzeltilemiyor.

Bu yüzden işletim sistemleri ve derleyiciler, hata **olsa bile** onun
zararını küçülten koruma katmanları ekler. Bu bölüm en yaygın üçünü
anlatıyor: **yığın kanaryası** (stack canary), **DEP** (veri yürütme
engeli) ve **ASLR** (adres alanı rastgeleleştirme). Hepsini yine Python'da
kurduğumuz oyuncak modellerle göreceğiz.

## Yığın ve dönüş bilgisi

Bir fonksiyon çağrılınca, onun yerel değişkenleri için bellekte bir alan
açılır; buna **yığın çerçevesi** (stack frame) denir. Çerçevede yerel
arabelleklerin hemen yanında, fonksiyon bitince programın **nereye
döneceğini** gösteren bilgi de durur. Bir taşma bu bilgiye ulaşırsa
programın akışı bozulur. Korumaların çoğu tam bu noktayı savunur.

## Yığın kanaryası

Madencilerin eski bir alışkanlığı vardır: ocağa bir kanarya götürürler,
tehlikeli gaz birikince ilk kanarya etkilenir ve madenciler uyarılır.
**Yığın kanaryası** aynı fikri kullanır: derleyici, arabellek ile dönüş
bilgisi arasına program her başladığında **rastgele** seçilen bir değer
koyar. Fonksiyon dönmeden önce bu değere bakar. Değer değişmişse arada bir
taşma olmuştur; program dönmek yerine hemen durdurulur.

```python
import random

rng = random.Random(42)
CANARY = rng.randrange(1, 256)


def make_frame(size):
    return [0] * size + [CANARY, 0]


def write(frame, data):
    for i, value in enumerate(data):
        if i < len(frame):
            frame[i] = value


def check(frame, size):
    if frame[size] != CANARY:
        return "stack smashing detected"
    return "ok"


small = make_frame(4)
write(small, [1, 2, 3])
print(check(small, 4))
big = make_frame(4)
write(big, [1, 2, 3, 4, 5, 6])
print(check(big, 4))
```

```text
ok
stack smashing detected
```

Çerçeve 4 sayılık arabellek, kanarya ve dönüş bilgisinden oluşuyor. Üç
sayı arabelleğe sığdı ve kanarya yerinde kaldı. Altı sayı ise arabelleği
aşıp kanaryanın üstüne yazdı; denetim bunu yakaladı. Gerçek programlarda
bu durumda `stack smashing detected` benzeri bir iletiyle program
sonlanır: bozulmuş bir dönüş bilgisiyle devam etmekten iyidir.

Kanaryanın **rastgele** ve **gizli** olması şarttır: herkesin bildiği sabit
bir değer, taşmayı fark etmeye yetmezdi. Kanarya yalnızca **dönüşten önce**
denetlendiği için, taşmanın aynı fonksiyon içinde bozduğu başka bir
değişkeni (önceki bölümdeki rol gibi) yakalayamaz.

## DEP: yazılabilen çalıştırılamaz

Bellek bölgelerinin her birinin izinleri vardır: okunabilir (`r`),
yazılabilir (`w`), çalıştırılabilir (`x`). **DEP** (Data Execution
Prevention, donanımdaki adıyla **NX** biti) şu kuralı uygular: veri için
ayrılmış bölgeler (yığın, öbek) **çalıştırılamaz**. Bunun genel adı
**W^X**'tir (write xor execute): bir bölge ya yazılabilir ya
çalıştırılabilir olur, ikisi birden değil.

```python
regions = {"code": "r-x", "data": "rw-", "stack": "rw-", "jit": "rwx"}
for name, perms in regions.items():
    writable = "w" in perms
    executable = "x" in perms
    flag = "  <- W^X violation" if writable and executable else ""
    print(f"{name:<6} {perms}{flag}")
```

```text
code   r-x
data   rw-
stack  rw-
jit    rwx  <- W^X violation
```

Kod bölgesi çalıştırılabilir ama yazılamaz; veri ve yığın yazılabilir ama
çalıştırılamaz. Böylece taşmayla belleğe yazılan veri, kod gibi
çalıştırılamaz. Listedeki `jit` bölgesi (çalışırken kod üreten
derleyicilerin kullandığı türden bir bölge) ikisine birden izin veriyor;
denetim onu işaretledi. Böyle bölgeler ancak gerçekten gerektiğinde ve
dikkatle açılır.

## ASLR: adresleri her seferinde değiştirmek

Taşmayı istismar etmeye çalışan biri, programın ve kütüphanelerin bellekte
**nerede** durduğunu bilmek ister. Eskiden bu adresler her çalıştırmada
aynıydı. **ASLR** (Address Space Layout Randomization) programın,
kütüphanelerin, yığının ve öbeğin başlangıç adresini her çalıştırmada
**rastgele** seçer:

```python
import random

for run in range(3):
    rng = random.Random(run)
    base = 0x400000 + rng.randrange(256) * 0x10000
    print(f"run {run}: base {base:#x}")
```

```text
run 0: base 0x1050000
run 1: base 0x840000
run 2: base 0x5c0000
```

Aynı program üç çalıştırmada üç farklı adreste başladı. Bir adres bir kez
öğrenilse bile bir sonraki çalıştırmada işe yaramaz.

ASLR'nin gücü, kaç farklı adresin mümkün olduğuna, yani **kaç bit
rastgelelik** (entropi) kullanıldığına bağlıdır:

```python
for bits in [8, 16, 28]:
    print(f"{bits:>2} bits: 1 in {2 ** bits:,}")
```

```text
 8 bits: 1 in 256
16 bits: 1 in 65,536
28 bits: 1 in 268,435,456
```

8 bitlik rastgelelikte doğru adresi tahmin etme şansı 256'da bir;
bu, birkaç yüz denemede tutturulabilir. Bit sayısı arttıkça olasılık hızla
düşer: her ek bit tahmin işini iki katına çıkarır. Bu yüzden 64 bitlik
sistemlerde ASLR, adres alanı dar olan 32 bitlik sistemlere göre çok daha
güçlüdür.

## Katmanlar birbirini tamamlar

<figure class="fig"><div class="flow">
  <span class="node">Taşma</span><span class="arrow">→</span>
  <span class="node acc">Kanarya: dönüşte yakalar</span><span class="arrow">→</span>
  <span class="node acc">DEP: veriyi çalıştırmaz</span><span class="arrow">→</span>
  <span class="node acc">ASLR: adresi gizler</span><span class="arrow">→</span>
  <span class="node ok">Program korunur</span>
</div><figcaption>Hiçbiri hatayı düzeltmez; her biri hatanın zarara dönüşmesini zorlaştırır.</figcaption></figure>

| Koruma | Neyi korur? | Nerede açılır? |
|---|---|---|
| **Yığın kanaryası** | Dönüş bilgisinin taşmayla bozulmasını yakalar | Derleyici (`-fstack-protector-strong`, `/GS`) |
| **DEP / NX** | Veri bölgelerinin kod gibi çalışmasını engeller | İşlemci + işletim sistemi |
| **ASLR** | Adresleri tahmin edilemez yapar | İşletim sistemi + konuma bağımsız derleme (PIE) |
| **CFI** (akış bütünlüğü) | Programın yalnızca izinli yerlere atlamasını sağlar | Derleyici + işletim sistemi |

Bu korumaların hiçbiri **hatayı düzeltmez**: taşma hâlâ oradadır. Her biri
yalnızca hatayı zarara dönüştürmeyi zorlaştırır. Bu yüzden birlikte
kullanılırlar (**katmanlı savunma**, defense in depth) ve bellek güvenli
dile geçmenin ya da hatayı düzeltmenin yerini tutmazlar. Bir koruma
kapatılarak derlenmiş bir program, güvenlik incelemesinde ilk işaretlenen
şeylerden biridir.

## Özet

- Korumalar bellek hatasını **düzeltmez**, zararını küçültür; birlikte
  kullanılır.
- **Yığın kanaryası:** arabellek ile dönüş bilgisi arasında rastgele,
  gizli bir değer; dönüşten önce denetlenir.
- **DEP / NX (W^X):** bir bölge ya yazılabilir ya çalıştırılabilir; veri
  kod gibi çalışmaz.
- **ASLR:** adresler her çalıştırmada rastgele; gücü bit sayısıyla artar,
  her bit tahmini iki katına çıkarır.
- Asıl çözüm yine **bellek güvenli kod**: korumalar ikinci savunma
  hattıdır.
