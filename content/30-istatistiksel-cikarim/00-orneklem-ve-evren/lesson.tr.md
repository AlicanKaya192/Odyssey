# Örneklem ve Evren

Bir uygulamanın kullanıcıları ortalama kaç dakika kalıyor? Yeni tasarım satışı
artırdı mı? Bu soruların cevabı **herkesi** ölçmekte. Ama çoğu zaman herkesi
ölçemezsin: çok pahalıdır, çok uzun sürer ya da herkes henüz ortada yoktur
(yarın gelecek kullanıcılar da soruya dahil). O yüzden **birkaçını** ölçer,
oradan **hepsi** hakkında bir şey söylersin.

İstatistiğin bu kısmına **çıkarım** (inference) denir: küçük bir parçadan
bütün hakkında, ne kadar emin olduğunu da söyleyerek, sonuç çıkarmak. Bu
modülün her bölümü bu tek fikrin bir parçası. İlk adım iki kelimeyi
ayırmak: **evren** ve **örneklem**.

## Evren ve örneklem

- **Evren** (population, bazen "ana kütle" de denir): hakkında bir şey
  söylemek istediğin grubun **tamamı**. Burada uygulamanın bütün
  kullanıcıları.
- **Örneklem** (sample): evrenden seçip gerçekten ölçtüğün kısım.

Bu patikada evreni biz kurduk: `ab_data.py` dosyasındaki `make_population`
uydurma bir alışveriş uygulamasının 100 000 kullanıcısını üretiyor. Sabit
tohumla (seed) çalıştığı için her bilgisayarda aynı sayılar çıkıyor. Gerçek
hayatta evren elinde olmaz; burada var, çünkü yöntemlerin **doğru** cevabı
bulup bulmadığını ancak doğru cevabı bilerek görebiliriz.

```python
from ab_data import make_population

users = make_population()
print(len(users))
print(users.head(3).to_string())
print(round(users["minutes"].mean(), 2))
print(round(users["bought"].mean(), 3))
```

```text
100000
   user_id  age  visits  minutes  bought  spend  load_ms
0  U000001   38       1     7.22       0    0.0      813
1  U000002   41       4     3.15       0    0.0      708
2  U000003   35       8    10.88       0    0.0      767
9.04
0.114
```

- Her satır bir kullanıcı. `minutes` ortalama oturum süresi (dakika),
  `visits` geçen ayki ziyaret sayısı, `bought` geçen ay alışveriş yaptıysa 1.
- Bütün kullanıcıların ortalama oturum süresi 9,04 dakika, alışveriş
  yapanların payı %11,4. Bu sayılar **evrenin** gerçek değerleri.

## Parametre ve istatistik

Evrenden hesaplanan sayıya **parametre** (parameter), örneklemden
hesaplanana **istatistik** (statistic) denir. İkisini karıştırmamak için
farklı harflerle yazılır:

| | Evren | Örneklem |
|---|---|---|
| Kaç kişi | $N$ | $n$ |
| Ortalama | $\mu$ ("mü") | $\bar{x}$ ("x bar") |
| Pay (oran) | $p$ | $\hat{p}$ ("p şapka") |
| Bilinir mi? | Neredeyse hiç | Her zaman: sen ölçtün |

Çıkarımın bütün işi şu: elindeki $\bar{x}$'ten bilmediğin $\mu$ hakkında
konuşmak.

## Her örneklem farklı bir cevap verir

Şimdi evreni bilmiyormuş gibi yapalım ve 100 kullanıcıyı rastgele seçelim.
`sample(n=100, random_state=...)` her kullanıcıya eşit seçilme şansı verir;
buna **basit rastgele örneklem** (simple random sample) denir.
`random_state` hangi 100 kişinin seçileceğini sabitler.

```python
from ab_data import make_population

users = make_population()
for seed in range(1, 6):
    sample = users.sample(n=100, random_state=seed)
    print(seed, round(sample["minutes"].mean(), 2))
```

```text
1 9.58
2 9.65
3 9.69
4 10.02
5 9.66
```

- Beş örneklem, beş farklı ortalama; hiçbiri tam 9,04 değil.
  Kodda hata yok: farklı 100 kişi farklı bir ortalama verir.
- Beşi de gerçeğin üstünde çıktı. Bu da şans: aşağıda bin örneklem çekince
  ortalamaların yaklaşık yarısının gerçeğin altına düştüğünü göreceğiz.
  Beş örneklemden bir yön çıkarmak, tek örneklemden çıkarmak kadar riskli.
- Örneklem istatistiğinin evrenin parametresinden şans yüzünden sapmasına
  **örnekleme hatası** (sampling error) denir. "Hata" kelimesi yanlış bir
  şey yapıldığını söylemez; rastgele seçimin doğal oynamasıdır.

## Tek örnekleme değil, binlercesine bak

Tek bir örneklemin ne kadar şanslı olduğunu bilemeyiz. Ama bu deneyi bin kez
tekrarlayabiliriz: her seferinde başka 100 kişi seç, ortalamasını not al.
Böylece örneklem ortalamasının **nasıl** oynadığını görürüz. Bu yönteme
**benzetim** (simulation) denir ve patika boyunca sık kullanacağız.

```python
import numpy as np
from ab_data import make_population

users = make_population()
true_mean = users["minutes"].mean()
for n in [25, 100, 400]:
    means = []
    for seed in range(1000):
        sample = users["minutes"].sample(n=n, random_state=seed)
        means.append(sample.mean())
    miss = np.abs(np.array(means) - true_mean)
    print(n, round(min(means), 2), round(max(means), 2),
          round(miss.mean(), 3), round((miss <= 1).mean(), 3))
```

```text
25 5.67 14.04 0.983 0.565
100 7.37 11.21 0.514 0.885
400 8.04 9.98 0.245 0.999
```

Sütunlar: örneklem büyüklüğü, bin ortalamanın en küçüğü ve en büyüğü,
ortalama ne kadar ıskaladığı (dakika) ve gerçeğe 1 dakikadan yakın olanların
payı.

- 25 kişilik örneklemlerde ortalama 5,67 ile 14,04 arasında
  gezdi; gerçeğe 1 dakikadan yakın olanların payı yalnızca %56,5.
- 400 kişide en küçük ortalama 8,04, en büyüğü 9,98 oldu;
  1 dakikanın içine düşenlerin payı %99,9.
- Ortalama ıskalama 25 kişide 0,98, 400 kişide 0,24
  dakika. Örneklem 16 kat büyüdü, ıskalama dört kat azaldı, 16 kat değil. Bu
  "karekök kuralını" Tahmin ve Standart Hata bölümünde ölçeceğiz.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="438.725781pt" height="227.257795pt" viewBox="0 0 438.725781 227.257795" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 227.257795 
L 438.725781 227.257795 
L 438.725781 0 
L 0 0 
L 0 227.257795 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 40.925781 187.524201 
L 431.525781 187.524201 
L 431.525781 10.116201 
L 40.925781 10.116201 
L 40.925781 187.524201 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 58.680327 187.524201 
L 66.571236 187.524201 
L 66.571236 185.00241 
L 58.680327 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_4">
    <path d="M 66.571236 187.524201 
L 74.462145 187.524201 
L 74.462145 187.524201 
L 66.571236 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_5">
    <path d="M 74.462145 187.524201 
L 82.353054 187.524201 
L 82.353054 182.480619 
L 74.462145 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_6">
    <path d="M 82.353054 187.524201 
L 90.243963 187.524201 
L 90.243963 182.480619 
L 82.353054 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_7">
    <path d="M 90.243963 187.524201 
L 98.134872 187.524201 
L 98.134872 167.349873 
L 90.243963 167.349873 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_8">
    <path d="M 98.134872 187.524201 
L 106.025781 187.524201 
L 106.025781 169.871664 
L 98.134872 169.871664 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_9">
    <path d="M 106.025781 187.524201 
L 113.91669 187.524201 
L 113.91669 157.262709 
L 106.025781 157.262709 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_10">
    <path d="M 113.91669 187.524201 
L 121.807599 187.524201 
L 121.807599 147.175545 
L 113.91669 147.175545 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_11">
    <path d="M 121.807599 187.524201 
L 129.698509 187.524201 
L 129.698509 139.610171 
L 121.807599 139.610171 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_12">
    <path d="M 129.698509 187.524201 
L 137.589418 187.524201 
L 137.589418 104.305097 
L 129.698509 104.305097 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_13">
    <path d="M 137.589418 187.524201 
L 145.480327 187.524201 
L 145.480327 99.261515 
L 137.589418 99.261515 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_14">
    <path d="M 145.480327 187.524201 
L 153.371236 187.524201 
L 153.371236 63.95644 
L 145.480327 63.95644 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_15">
    <path d="M 153.371236 187.524201 
L 161.262145 187.524201 
L 161.262145 56.391067 
L 153.371236 56.391067 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_16">
    <path d="M 161.262145 187.524201 
L 169.153054 187.524201 
L 169.153054 81.608977 
L 161.262145 81.608977 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_17">
    <path d="M 169.153054 187.524201 
L 177.043963 187.524201 
L 177.043963 63.95644 
L 169.153054 63.95644 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_18">
    <path d="M 177.043963 187.524201 
L 184.934872 187.524201 
L 184.934872 46.303903 
L 177.043963 46.303903 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_19">
    <path d="M 184.934872 187.524201 
L 192.825781 187.524201 
L 192.825781 23.607783 
L 184.934872 23.607783 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_20">
    <path d="M 192.825781 187.524201 
L 200.71669 187.524201 
L 200.71669 43.782112 
L 192.825781 43.782112 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_21">
    <path d="M 200.71669 187.524201 
L 208.607599 187.524201 
L 208.607599 18.564201 
L 200.71669 18.564201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_22">
    <path d="M 208.607599 187.524201 
L 216.498509 187.524201 
L 216.498509 48.825694 
L 208.607599 48.825694 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_23">
    <path d="M 216.498509 187.524201 
L 224.389418 187.524201 
L 224.389418 36.216739 
L 216.498509 36.216739 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_24">
    <path d="M 224.389418 187.524201 
L 232.280327 187.524201 
L 232.280327 79.087186 
L 224.389418 79.087186 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_25">
    <path d="M 232.280327 187.524201 
L 240.171236 187.524201 
L 240.171236 84.130768 
L 232.280327 84.130768 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_26">
    <path d="M 240.171236 187.524201 
L 248.062145 187.524201 
L 248.062145 106.826888 
L 240.171236 106.826888 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_27">
    <path d="M 248.062145 187.524201 
L 255.953054 187.524201 
L 255.953054 79.087186 
L 248.062145 79.087186 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_28">
    <path d="M 255.953054 187.524201 
L 263.843963 187.524201 
L 263.843963 132.044798 
L 255.953054 132.044798 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_29">
    <path d="M 263.843963 187.524201 
L 271.734872 187.524201 
L 271.734872 109.348679 
L 263.843963 109.348679 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_30">
    <path d="M 271.734872 187.524201 
L 279.625781 187.524201 
L 279.625781 129.523007 
L 271.734872 129.523007 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_31">
    <path d="M 279.625781 187.524201 
L 287.51669 187.524201 
L 287.51669 144.653753 
L 279.625781 144.653753 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_32">
    <path d="M 287.51669 187.524201 
L 295.407599 187.524201 
L 295.407599 157.262709 
L 287.51669 157.262709 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_33">
    <path d="M 295.407599 187.524201 
L 303.298509 187.524201 
L 303.298509 154.740918 
L 295.407599 154.740918 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_34">
    <path d="M 303.298509 187.524201 
L 311.189418 187.524201 
L 311.189418 167.349873 
L 303.298509 167.349873 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_35">
    <path d="M 311.189418 187.524201 
L 319.080327 187.524201 
L 319.080327 159.7845 
L 311.189418 159.7845 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_36">
    <path d="M 319.080327 187.524201 
L 326.971236 187.524201 
L 326.971236 172.393455 
L 319.080327 172.393455 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_37">
    <path d="M 326.971236 187.524201 
L 334.862145 187.524201 
L 334.862145 185.00241 
L 326.971236 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_38">
    <path d="M 334.862145 187.524201 
L 342.753054 187.524201 
L 342.753054 182.480619 
L 334.862145 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_39">
    <path d="M 342.753054 187.524201 
L 350.643963 187.524201 
L 350.643963 182.480619 
L 342.753054 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_40">
    <path d="M 350.643963 187.524201 
L 358.534872 187.524201 
L 358.534872 179.958828 
L 350.643963 179.958828 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_41">
    <path d="M 358.534872 187.524201 
L 366.425781 187.524201 
L 366.425781 187.524201 
L 358.534872 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_42">
    <path d="M 366.425781 187.524201 
L 374.31669 187.524201 
L 374.31669 187.524201 
L 366.425781 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_43">
    <path d="M 374.31669 187.524201 
L 382.207599 187.524201 
L 382.207599 185.00241 
L 374.31669 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_44">
    <path d="M 382.207599 187.524201 
L 390.098509 187.524201 
L 390.098509 187.524201 
L 382.207599 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_45">
    <path d="M 390.098509 187.524201 
L 397.989418 187.524201 
L 397.989418 187.524201 
L 390.098509 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_46">
    <path d="M 397.989418 187.524201 
L 405.880327 187.524201 
L 405.880327 187.524201 
L 397.989418 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_47">
    <path d="M 405.880327 187.524201 
L 413.771236 187.524201 
L 413.771236 182.480619 
L 405.880327 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_48">
    <path d="M 159.156842 187.524201 
L 160.98964 187.524201 
L 160.98964 185.00241 
L 159.156842 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_49">
    <path d="M 160.98964 187.524201 
L 162.822438 187.524201 
L 162.822438 185.00241 
L 160.98964 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_50">
    <path d="M 162.822438 187.524201 
L 164.655236 187.524201 
L 164.655236 187.524201 
L 162.822438 187.524201 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_51">
    <path d="M 164.655236 187.524201 
L 166.488034 187.524201 
L 166.488034 185.00241 
L 164.655236 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_52">
    <path d="M 166.488034 187.524201 
L 168.320832 187.524201 
L 168.320832 185.00241 
L 166.488034 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_53">
    <path d="M 168.320832 187.524201 
L 170.15363 187.524201 
L 170.15363 185.00241 
L 168.320832 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_54">
    <path d="M 170.15363 187.524201 
L 171.986428 187.524201 
L 171.986428 185.00241 
L 170.15363 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_55">
    <path d="M 171.986428 187.524201 
L 173.819226 187.524201 
L 173.819226 182.480619 
L 171.986428 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_56">
    <path d="M 173.819226 187.524201 
L 175.652024 187.524201 
L 175.652024 167.349873 
L 173.819226 167.349873 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_57">
    <path d="M 175.652024 187.524201 
L 177.484822 187.524201 
L 177.484822 172.393455 
L 175.652024 172.393455 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_58">
    <path d="M 177.484822 187.524201 
L 179.31762 187.524201 
L 179.31762 164.828082 
L 177.484822 164.828082 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_59">
    <path d="M 179.31762 187.524201 
L 181.150418 187.524201 
L 181.150418 142.131962 
L 179.31762 142.131962 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_60">
    <path d="M 181.150418 187.524201 
L 182.983216 187.524201 
L 182.983216 142.131962 
L 181.150418 142.131962 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_61">
    <path d="M 182.983216 187.524201 
L 184.816014 187.524201 
L 184.816014 111.87047 
L 182.983216 111.87047 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_62">
    <path d="M 184.816014 187.524201 
L 186.648812 187.524201 
L 186.648812 116.914052 
L 184.816014 116.914052 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_63">
    <path d="M 186.648812 187.524201 
L 188.48161 187.524201 
L 188.48161 124.479425 
L 186.648812 124.479425 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_64">
    <path d="M 188.48161 187.524201 
L 190.314408 187.524201 
L 190.314408 91.696142 
L 188.48161 91.696142 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_65">
    <path d="M 190.314408 187.524201 
L 192.147205 187.524201 
L 192.147205 74.043604 
L 190.314408 74.043604 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_66">
    <path d="M 192.147205 187.524201 
L 193.980003 187.524201 
L 193.980003 58.912858 
L 192.147205 58.912858 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_67">
    <path d="M 193.980003 187.524201 
L 195.812801 187.524201 
L 195.812801 106.826888 
L 193.980003 106.826888 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_68">
    <path d="M 195.812801 187.524201 
L 197.645599 187.524201 
L 197.645599 61.434649 
L 195.812801 61.434649 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_69">
    <path d="M 197.645599 187.524201 
L 199.478397 187.524201 
L 199.478397 28.651365 
L 197.645599 28.651365 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_70">
    <path d="M 199.478397 187.524201 
L 201.311195 187.524201 
L 201.311195 26.129574 
L 199.478397 26.129574 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_71">
    <path d="M 201.311195 187.524201 
L 203.143993 187.524201 
L 203.143993 36.216739 
L 201.311195 36.216739 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_72">
    <path d="M 203.143993 187.524201 
L 204.976791 187.524201 
L 204.976791 71.521813 
L 203.143993 71.521813 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_73">
    <path d="M 204.976791 187.524201 
L 206.809589 187.524201 
L 206.809589 84.130768 
L 204.976791 84.130768 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_74">
    <path d="M 206.809589 187.524201 
L 208.642387 187.524201 
L 208.642387 53.869276 
L 206.809589 53.869276 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_75">
    <path d="M 208.642387 187.524201 
L 210.475185 187.524201 
L 210.475185 71.521813 
L 208.642387 71.521813 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_76">
    <path d="M 210.475185 187.524201 
L 212.307983 187.524201 
L 212.307983 76.565395 
L 210.475185 76.565395 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_77">
    <path d="M 212.307983 187.524201 
L 214.140781 187.524201 
L 214.140781 106.826888 
L 212.307983 106.826888 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_78">
    <path d="M 214.140781 187.524201 
L 215.973579 187.524201 
L 215.973579 101.783306 
L 214.140781 101.783306 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_79">
    <path d="M 215.973579 187.524201 
L 217.806377 187.524201 
L 217.806377 109.348679 
L 215.973579 109.348679 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_80">
    <path d="M 217.806377 187.524201 
L 219.639175 187.524201 
L 219.639175 116.914052 
L 217.806377 116.914052 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_81">
    <path d="M 219.639175 187.524201 
L 221.471973 187.524201 
L 221.471973 134.566589 
L 219.639175 134.566589 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_82">
    <path d="M 221.471973 187.524201 
L 223.304771 187.524201 
L 223.304771 134.566589 
L 221.471973 134.566589 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_83">
    <path d="M 223.304771 187.524201 
L 225.137569 187.524201 
L 225.137569 149.697336 
L 223.304771 149.697336 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_84">
    <path d="M 225.137569 187.524201 
L 226.970367 187.524201 
L 226.970367 159.7845 
L 225.137569 159.7845 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_85">
    <path d="M 226.970367 187.524201 
L 228.803165 187.524201 
L 228.803165 174.915246 
L 226.970367 174.915246 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_86">
    <path d="M 228.803165 187.524201 
L 230.635963 187.524201 
L 230.635963 169.871664 
L 228.803165 169.871664 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_87">
    <path d="M 230.635963 187.524201 
L 232.468761 187.524201 
L 232.468761 174.915246 
L 230.635963 174.915246 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_88">
    <path d="M 232.468761 187.524201 
L 234.301559 187.524201 
L 234.301559 182.480619 
L 232.468761 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_89">
    <path d="M 234.301559 187.524201 
L 236.134357 187.524201 
L 236.134357 185.00241 
L 234.301559 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_90">
    <path d="M 236.134357 187.524201 
L 237.967155 187.524201 
L 237.967155 185.00241 
L 236.134357 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_91">
    <path d="M 237.967155 187.524201 
L 239.799953 187.524201 
L 239.799953 185.00241 
L 237.967155 185.00241 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_92">
    <path d="M 239.799953 187.524201 
L 241.632751 187.524201 
L 241.632751 182.480619 
L 239.799953 182.480619 
z
" clip-path="url(#pa05f87269e)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="72.595478" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="72.595478" y="202.121858" transform="rotate(-0 72.595478 202.121858)">6</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="157.443963" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="157.443963" y="202.121858" transform="rotate(-0 157.443963 202.121858)">8</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="242.292448" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="242.292448" y="202.121858" transform="rotate(-0 242.292448 202.121858)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="327.140933" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="327.140933" y="202.121858" transform="rotate(-0 327.140933 202.121858)">12</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="411.989418" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="411.989418" y="202.121858" transform="rotate(-0 411.989418 202.121858)">14</text>
     </g>
    </g>
    <g id="text_6">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="236.225781" y="217.655451" transform="rotate(-0 236.225781 217.655451)">Örneklem ortalaması (dakika)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_6">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="191.323029" transform="rotate(-0 33.925781 191.323029)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="162.306291" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="166.105119" transform="rotate(-0 33.925781 166.105119)">10</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="137.08838" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="140.887208" transform="rotate(-0 33.925781 140.887208)">20</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="111.87047" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="115.669298" transform="rotate(-0 33.925781 115.669298)">30</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="86.652559" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="90.451388" transform="rotate(-0 33.925781 90.451388)">40</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="61.434649" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="65.233477" transform="rotate(-0 33.925781 65.233477)">50</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="36.216739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="40.015567" transform="rotate(-0 33.925781 40.015567)">60</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="14.797656" transform="rotate(-0 33.925781 14.797656)">70</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="98.820201" transform="rotate(-90 14.798438 98.820201)">Kaç örneklemde</text>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 201.669853 187.524201 
L 201.669853 10.116201 
" clip-path="url(#pa05f87269e)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_93">
    <path d="M 40.925781 187.524201 
L 40.925781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_94">
    <path d="M 431.525781 187.524201 
L 431.525781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_95">
    <path d="M 40.925781 187.524201 
L 431.525781 187.524201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_96">
    <path d="M 40.925781 10.116201 
L 431.525781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_97">
     <path d="M 354.364844 26.714639 
L 374.364844 26.714639 
L 374.364844 19.714639 
L 354.364844 19.714639 
z
" style="fill: #1f77b4; opacity: 0.65"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.364844" y="26.714639" transform="rotate(-0 382.364844 26.714639)">n = 25</text>
    </g>
    <g id="patch_98">
     <path d="M 354.364844 41.71542 
L 374.364844 41.71542 
L 374.364844 34.71542 
L 354.364844 34.71542 
z
" style="fill: #ff7f0e; opacity: 0.65"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.364844" y="41.71542" transform="rotate(-0 382.364844 41.71542)">n = 400</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa05f87269e">
   <rect x="40.925781" y="10.116201" width="390.6" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Bin örneklemin ortalaması. Kesik çizgi evrenin gerçek ortalaması. 400 kişilik örneklemler (turuncu) gerçeğin çok daha yakınında toplanıyor.</figcaption>
</figure>

## Yanlı örneklem: büyütmek kurtarmaz

Örnekleme hatası örneklem büyüdükçe küçülür. Ama başka bir hata türü
küçülmez. Diyelim ki anketi yalnızca **beşinci ziyaretinden sonra**
kullanıcılara gösterdin. Örneklem rastgele değil: sık gelenler seçiliyor ve
uygulamada sık gelenler daha uzun kalıyor.

```python
import numpy as np
from ab_data import make_population

users = make_population()
heavy = users[users["visits"] >= 5]
print(len(heavy))
for n in [100, 1000, 10000]:
    biased, fair = [], []
    for seed in range(200):
        biased.append(heavy["minutes"].sample(n=n, random_state=seed).mean())
        fair.append(users["minutes"].sample(n=n, random_state=seed).mean())
    print(n, round(np.mean(biased), 2), round(np.mean(fair), 2))
```

```text
18470
100 10.91 9.08
1000 10.94 9.06
10000 10.94 9.04
```

- Her örneklem büyüklüğünde 200 tekrar yaptık. Sağdaki sütun (rastgele
  örneklem) gerçeğin (9,04) çevresinde.
- Ortadaki sütun (yalnızca sık gelenler) 100 kişide de 10 000 kişide de
  10,9 civarında: gerçeğin yaklaşık 2 dakika üstünde.
- Sistematik olarak aynı yöne kayan bu hataya **yanlılık** (bias) denir.
  Daha çok kişi sormak onu düzeltmez; yalnızca yanlış cevaptan daha emin
  yapar. Çare **seçimin kendisini** düzeltmek: herkese eşit şans vermek.

<figure class="fig">
<div class="versus">
<div class="ok"><h4>Örnekleme hatası</h4>
<p>Şanstan gelir, yönü her seferinde farklıdır.</p>
<p>Örneklem büyüdükçe küçülür.</p>
<p>Ne kadar olduğu hesaplanabilir.</p></div>
<div class="no"><h4>Yanlılık</h4>
<p>Seçim biçiminden gelir, hep aynı yöne iter.</p>
<p>Örneklem büyüse de kalır.</p>
<p>Veriden fark edilmez; seçime bakılır.</p></div>
</div>
<figcaption>İki hata türü. İstatistik ilkini ölçer; ikincisini ancak iyi
tasarım önler.</figcaption>
</figure>

## Özet

- **Evren** soru sorduğun grubun tamamı, **örneklem** ölçtüğün kısmı.
  Evrenin sayısı **parametre** ($\mu$, $p$), örneklemin sayısı
  **istatistik** ($\bar{x}$, $\hat{p}$).
- Rastgele örneklemler birbirinden farklı sonuç verir (**örnekleme
  hatası**); örneklem büyüdükçe bu oynama azalır.
- Seçim biçimi bir grubu kayırıyorsa sonuç hep aynı yöne kayar
  (**yanlılık**); örneklemi büyütmek bunu düzeltmez.
- Tek bir örnekleme bakarak şanslı mı şanssız mı olduğunu bilemezsin;
  benzetimle binlerce örneklem çekip davranışı görebilirsin.
