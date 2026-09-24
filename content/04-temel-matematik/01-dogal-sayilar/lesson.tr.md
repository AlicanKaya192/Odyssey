# Doğal Sayılar ve İşlem Önceliği

Saymayı öğrendiğimiz sayılar, matematiğin temeli: $0, 1, 2, 3, \dots$ Bu
bölümde onları bir kez daha, ama bu kez "neden böyle?" sorusuyla ele
alacağız: sayıları nasıl yazdığımız (basamak değeri), dört işlemin
kuralları, kalanlı bölme ve en önemlisi **işlem önceliği**: bir ifadede
hangi işlemin önce yapıldığı.

İşlem önceliği küçük bir kural gibi görünüyor ama çok önemli. Aynı
ifadeyi iki kişi farklı sırayla hesaplarsa iki farklı sonuç bulur; kural
herkesin aynı sonucu bulmasını sağlıyor. Bilgisayarlar ve hesap
makineleri de bu kurala göre çalışıyor.

Ön bilgi: Matematiği Okumak bölümü.

## Sayıları yazmak: basamak değeri

On tane **rakamla** ($0, 1, 2, \dots, 9$) sonsuz sayıda **sayı**
yazabiliyoruz. Bunu mümkün kılan fikir **basamak değeri**: bir rakamın
değeri, sayının içinde **nerede durduğuna** bağlı.

<figure class="fig">
<svg viewBox="0 0 420 154" width="420"><rect class="box" x="14" y="58" width="56" height="48"/><text class="ink" x="42.0" y="91" font-size="24" text-anchor="middle">3</text><text class="dim" x="42.0" y="49" font-size="10" text-anchor="middle">milyon</text><rect class="box" x="70" y="58" width="56" height="48"/><text class="ink" x="98.0" y="91" font-size="24" text-anchor="middle">7</text><text class="dim" x="98.0" y="36" font-size="10" text-anchor="middle">yüz</text><text class="dim" x="98.0" y="49" font-size="10" text-anchor="middle">bin</text><rect class="box" x="126" y="58" width="56" height="48"/><text class="ink" x="154.0" y="91" font-size="24" text-anchor="middle">0</text><text class="dim" x="154.0" y="36" font-size="10" text-anchor="middle">on</text><text class="dim" x="154.0" y="49" font-size="10" text-anchor="middle">bin</text><rect class="box" x="182" y="58" width="56" height="48"/><text class="ink" x="210.0" y="91" font-size="24" text-anchor="middle">5</text><text class="dim" x="210.0" y="49" font-size="10" text-anchor="middle">bin</text><rect class="box" x="238" y="58" width="56" height="48"/><text class="ink" x="266.0" y="91" font-size="24" text-anchor="middle">8</text><text class="dim" x="266.0" y="49" font-size="10" text-anchor="middle">yüz</text><rect class="box" x="294" y="58" width="56" height="48"/><text class="ink" x="322.0" y="91" font-size="24" text-anchor="middle">1</text><text class="dim" x="322.0" y="49" font-size="10" text-anchor="middle">on</text><rect class="box" x="350" y="58" width="56" height="48"/><text class="ink" x="378.0" y="91" font-size="24" text-anchor="middle">2</text><text class="dim" x="378.0" y="49" font-size="10" text-anchor="middle">bir</text><rect class="curve" x="67" y="55" width="62" height="54" rx="4"/><text class="ink" x="210.0" y="140" font-size="12" text-anchor="middle">7'nin basamak değeri: 7 × 100 000 = 700 000</text></svg>
  <figcaption>$3\,705\,812$ sayısında her rakamın bir basamağı var. 7 yüz binler basamağında, bu yüzden değeri 7 değil 700 000. 0, o basamakta hiçbir şey olmadığını söylüyor ama yerini tutuyor.</figcaption>
</figure>

Her basamak, sağındakinin **10 katı**. Bu yüzden sistemimize **onluk
sistem** denir. Bir sayı, rakamlarının basamak değerleriyle çarpılıp
toplanmasıdır:

$$
3\,705\,812 = 3 \cdot 1\,000\,000 + 7 \cdot 100\,000 + 0 \cdot 10\,000 + 5 \cdot 1\,000 + 8 \cdot 100 + 1 \cdot 10 + 2
$$

**Rakam ile sayı farkı:** $7$ bir rakamdır ve aynı zamanda bir sayıdır;
$705$ bir sayıdır ve üç rakamdan oluşur. "Kaç basamaklı?" sorusu, sayının
kaç rakamla yazıldığını sorar: $3\,705\,812$ yedi basamaklı.

**Sıfırın görevi:** $705$ ile $75$ farklı sayılar. $705$'teki $0$, onlar
basamağının boş olduğunu söyler ve $7$'yi yüzler basamağında tutar.
Sıfır olmasaydı bu iki sayıyı yazıda ayıramazdık.

**Büyük sayıları okumak:** Sağdan başlayarak üçer üçer grupla: $3\,705\,812$
"üç milyon yedi yüz beş bin sekiz yüz on iki". Bu derste grupları küçük
boşlukla ayırıyoruz; Türkçede nokta ($3.705.812$), İngilizcede virgül
($3{,}705{,}812$) da kullanılır.

## Dört işlem ve adları

| İşlem | Parçaları | Örnek |
|---|---|---|
| Toplama | toplanan $+$ toplanan $=$ **toplam** | $8 + 5 = 13$ |
| Çıkarma | eksilen $-$ çıkan $=$ **fark** | $13 - 5 = 8$ |
| Çarpma | çarpan $\times$ çarpan $=$ **çarpım** | $4 \cdot 6 = 24$ |
| Bölme | bölünen $\div$ bölen $=$ **bölüm** | $24 \div 6 = 4$ |

Çarpma **tekrarlı toplama**dır: $4 \cdot 6 = 6 + 6 + 6 + 6$. Bölme de
çarpmanın tersi: $24 \div 6$, "hangi sayıyı $6$ ile çarparsam $24$
olur?" sorusu.

## İşlemlerin özellikleri

Bu özellikler hesabı kolaylaştıran kısayolların kaynağı ve cebirde
harflerle çalışırken sürekli kullanacağımız kurallar.

| Özellik | Kural | Örnek |
|---|---|---|
| Değişme | $a + b = b + a$ ve $a \cdot b = b \cdot a$ | $7 \cdot 4 = 4 \cdot 7$ |
| Birleşme | $(a + b) + c = a + (b + c)$, $(ab)c = a(bc)$ | $(25 \cdot 4) \cdot 7 = 25 \cdot (4 \cdot 7)$ |
| Dağılma | $a(b + c) = ab + ac$ | $7 \cdot 13 = 7 \cdot 10 + 7 \cdot 3$ |
| Etkisiz eleman | $a + 0 = a$, $a \cdot 1 = a$ | $58 \cdot 1 = 58$ |
| Yutan eleman | $a \cdot 0 = 0$ | $1\,000 \cdot 0 = 0$ |

**Çıkarma ve bölmede değişme yok:** $8 - 5 = 3$ ama $5 - 8 = -3$;
$12 \div 4 = 3$ ama $4 \div 12 = \tfrac{1}{3}$. Birleşme de yok:
$(12 - 5) - 2 = 5$ ama $12 - (5 - 2) = 9$.

### Dağılma özelliği neden doğru?

<figure class="fig">
<svg viewBox="0 0 380 212" width="380"><rect class="dot" opacity="0.22" x="60" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="60" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="80" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="100" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="120" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="140" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="160" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="180" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="200" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="220" y="150" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="30" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="50" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="70" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="90" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="110" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="130" width="18" height="18" rx="2"/><rect class="dot" opacity="0.22" x="240" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="260" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="280" y="150" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="30" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="50" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="70" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="90" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="110" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="130" width="18" height="18" rx="2"/><rect class="dot2" opacity="0.22" x="300" y="150" width="18" height="18" rx="2"/><rect class="curve" x="57" y="27" width="202" height="144" rx="4"/><rect class="curve2" x="259" y="27" width="62" height="144" rx="4"/><text class="ink" x="160" y="106.0" font-size="14" text-anchor="middle">7 × 10 = 70</text><text class="ink" x="290.0" y="106.0" font-size="14" text-anchor="middle">21</text><text class="ink" x="46" y="105.0" font-size="14" text-anchor="middle">7</text><text class="ink" x="160" y="18" font-size="13" text-anchor="middle">10</text><text class="ink" x="290.0" y="18" font-size="13" text-anchor="middle">3</text><text class="ink" x="190.0" y="198" font-size="13" text-anchor="middle">7 × 13 = 7 × 10 + 7 × 3 = 70 + 21 = 91</text></svg>
  <figcaption>$7$ satır ve $13$ sütunluk bir dikdörtgende $7 \cdot 13$ kare var. Dikdörtgeni $10$ ve $3$ sütunluk iki parçaya bölünce $7 \cdot 10 = 70$ mor ve $7 \cdot 3 = 21$ turuncu kare çıkıyor: toplam $91$.</figcaption>
</figure>

Dağılma özelliği zihinden hesabın en güçlü aracı:

$$
\begin{aligned}
99 \cdot 7 &= (100 - 1) \cdot 7 = 700 - 7 = 693 \\
25 \cdot 44 &= 25 \cdot 4 \cdot 11 = 100 \cdot 11 = 1\,100 \\
38 \cdot 25 + 62 \cdot 25 &= (38 + 62) \cdot 25 = 100 \cdot 25 = 2\,500
\end{aligned}
$$

Son satırda özelliği **tersten** kullandık: ortak çarpanı ($25$) dışarı
aldık. Cebirde buna **ortak paranteze almak** denecek.

### Sıfıra bölme tanımsız

$12 \div 0$ ne olabilir? Bölme çarpmanın tersiydi: "hangi sayıyı $0$ ile
çarparsam $12$ olur?" Hiçbir sayı; çünkü her sayı $0$ ile çarpılınca $0$
olur. Bu yüzden sıfıra bölme **tanımsızdır**: bir sonucu yok. $0 \div 12
= 0$ ise sorunsuz: $0 \cdot 12 = 0$.

## Kalanlı bölme

Her bölme tam çıkmaz. $1\,000$ kalemi $37$ öğrenciye eşit dağıtırsak her
öğrenci $27$ kalem alır ve $1$ kalem artar:

$$
1\,000 = 37 \cdot 27 + 1
$$

Genel olarak bir $a$ sayısını $b$'ye bölmek, $a$'yı şöyle yazmak
demektir:

$$
a = b \cdot q + r, \qquad 0 \le r < b
$$

$q$ **bölüm**, $r$ **kalan**. Kalan her zaman bölenden küçüktür; öyle
olmasaydı bir kez daha bölebilirdik.

**Sağlama:** Bölümü bölenle çarp, kalanı ekle; bölüneni bulmalısın:
$37 \cdot 27 + 1 = 999 + 1 = 1\,000$ ✓.

Kalan günlük hayatta sık geçer: $100$ gün sonra haftanın hangi günü?
$100 = 7 \cdot 14 + 2$: $14$ tam hafta ve $2$ gün. Bugün pazartesiyse
$100$ gün sonra çarşamba.

## İşlem önceliği

Şu ifadenin değeri ne?

$$
2 + 3 \cdot 4
$$

Soldan sağa gidersek $5 \cdot 4 = 20$; çarpmayı önce yaparsak $2 + 12 =
14$. İkisi aynı olamaz; matematik bir kurala karar vermiş: **çarpma,
toplamadan önce**. Doğru cevap $14$.

Bütün kural dört adımda:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1. Parantez</b><br>içten dışa</span>
    <span class="arrow">→</span>
    <span class="node"><b>2. Üs</b><br>ve kök</span>
    <span class="arrow">→</span>
    <span class="node"><b>3. Çarpma, bölme</b><br>soldan sağa</span>
    <span class="arrow">→</span>
    <span class="node"><b>4. Toplama, çıkarma</b><br>soldan sağa</span>
  </div>
  <figcaption>Önce parantezlerin içi, sonra üsler, sonra çarpma ve bölme, en son toplama ve çıkarma. Aynı basamaktaki işlemler (çarpma ile bölme, toplama ile çıkarma) soldan sağa sırayla yapılır.</figcaption>
</figure>

**Üs** tekrarlı çarpmadır: $4^2 = 4 \cdot 4 = 16$, $2^3 = 2 \cdot 2 \cdot 2
= 8$. Ayrıntısıyla Üslü Sayılar bölümünde göreceğiz; burada yalnızca
önceliğini bilmek yeterli.

### Örnekler

**Çarpma toplamadan önce:**

$$
2 + 3 \cdot 4^2 = 2 + 3 \cdot 16 = 2 + 48 = 50
$$

Önce üs ($4^2 = 16$), sonra çarpma, en son toplama.

**Çarpma ve bölme eşit öncelikli: soldan sağa.**

$$
8 \div 2 \cdot 4 = 4 \cdot 4 = 16
$$

$8 \div (2 \cdot 4) = 1$ **değil**. "Çarpma bölmeden önce" diye bir kural
yok; ikisi aynı basamakta ve soldan sağa yapılıyor.

**Toplama ve çıkarma da soldan sağa.**

$$
10 - 4 + 3 = 6 + 3 = 9
$$

$10 - (4 + 3) = 3$ **değil**.

**Parantez her şeyi değiştirir:**

$$
18 - 2 \cdot (3 + 4) + 12 \div 3 = 18 - 2 \cdot 7 + 4 = 18 - 14 + 4 = 8
$$

Adım adım: parantez ($3 + 4 = 7$), çarpma ve bölme ($2 \cdot 7 = 14$,
$12 \div 3 = 4$), en son soldan sağa toplama ve çıkarma.

**İç içe parantez: içten dışa.**

$$
\begin{aligned}
5 \cdot [20 - (2 + 3) \cdot 3] &= 5 \cdot [20 - 5 \cdot 3] \\
&= 5 \cdot [20 - 15] \\
&= 5 \cdot 5 = 25
\end{aligned}
$$

### Terimlere bölmek: güvenli bir yöntem

Uzun bir ifadede önce **parantez dışındaki $+$ ve $-$ işaretlerinden**
böl. Her parçayı (terimi) ayrı hesapla, sonra topla:

$$
\underbrace{18}_{18} \; - \; \underbrace{2 \cdot (3 + 4)}_{14} \; + \; \underbrace{12 \div 3}_{4} = 18 - 14 + 4 = 8
$$

Bu yöntem işlem önceliğini kendiliğinden uyguluyor, çünkü çarpma ve
bölme hep bir terimin içinde kalıyor.

## Tahmin ve yuvarlama

Bir hesabın sonucunun **makul** olup olmadığını anlamak için sayıları
yuvarlayıp kabaca hesapla. $38 \cdot 51$'in kaba değeri $40 \cdot 50 =
2\,000$; gerçek sonuç $1\,938$. Hesap sonunda $19\,380$ ya da $193$
bulsaydın bir hata yaptığını hemen anlardın.

Tam sayıları en yakın ona ya da yüze yuvarlamak: $738 \approx 740$ (en
yakın on), $738 \approx 700$ (en yakın yüz). Birler basamağı $5$ ya da
büyükse yukarı, küçükse aşağı. Ondalık sayılarda yuvarlamayı kendi
bölümünde göreceğiz.

## Makine öğrenmesinde doğal sayılar

**Parametre saymak.** Bir sinir ağı katmanı $784$ girdiyi $128$ nörona
bağlıyorsa $784 \cdot 128$ ağırlık ve her nöron için bir sabit, yani
$128$ sabit terim var:

$$
784 \cdot 128 + 128 = 100\,352 + 128 = 100\,480
$$

Dağılma özelliğiyle daha kısa: $128 \cdot (784 + 1) = 128 \cdot 785$.
Büyük dil modellerinde bu sayı milyarları buluyor.

**Kalanlı bölme ve yığınlar.** $10\,000$ örnekli bir veri seti $32$'lik
yığınlar (batch) hâlinde işlenirse:

$$
10\,000 = 32 \cdot 312 + 16
$$

$312$ tam yığın ve $16$ örnekli son bir yığın var; bir tur (epoch) $313$
adım sürüyor.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>$2 + 3 \cdot 4 = 20$</p>
      <p>$8 \div 2 \cdot 4 = 1$</p>
      <p>$10 - 4 + 3 = 3$</p>
      <p>$12 \div 0 = 0$</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>Çarpma önce: $2 + 12 = 14$</p>
      <p>Soldan sağa: $4 \cdot 4 = 16$</p>
      <p>Soldan sağa: $6 + 3 = 9$</p>
      <p>Sıfıra bölme tanımsız</p>
    </div>
  </div>
  <figcaption>Aynı basamaktaki işlemlerde sıra hep soldan sağa.</figcaption>
</figure>

- **"Çarpma bölmeden, toplama çıkarmadan önce" sanmak.** İkisi de eşit
  öncelikli; soldan sağa yapılır.
- **Kalanı bölenden büyük bırakmak.** $50 \div 7$ için "bölüm 6, kalan
  8" yanlış; $8 \ge 7$, bir kez daha bölünür: bölüm $7$, kalan $1$.
- **Basamak değerini karıştırmak.** $3\,705\,812$'deki $7$'nin değeri
  $700\,000$, $7\,000$ değil.

## Özet

- Onluk sistem: her basamak sağındakinin 10 katı; rakamın değeri yerine bağlı.
- Toplam, fark, çarpım, bölüm; çarpma tekrarlı toplama, bölme çarpmanın tersi.
- Değişme ve birleşme toplamada ve çarpmada var, çıkarmada ve bölmede yok.
- Dağılma: $a(b + c) = ab + ac$; zihinden hesabın ve ortak paranteze almanın temeli.
- Sıfıra bölme tanımsız; $0 \div a = 0$.
- Kalanlı bölme: $a = bq + r$, $0 \le r < b$; sağlama $bq + r$.
- İşlem önceliği: parantez → üs → çarpma/bölme (soldan sağa) → toplama/çıkarma (soldan sağa).
- Uzun ifadeleri parantez dışındaki $+$ ve $-$'den terimlere böl.
- Sonucu kaba bir tahminle karşılaştır.
