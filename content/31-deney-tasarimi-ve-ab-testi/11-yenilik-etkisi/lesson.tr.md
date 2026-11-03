# Yenilik Etkisi ve Uzun Vadeli Etki

Bir A/B testi kısa bir pencereden bakar: iki hafta, bir ay. Kararın etkisi
ise aylarca sürer. Bu ikisi her zaman aynı şeyi söylemez. Yeni bir düğme
ya da yeni bir tasarım ilk günlerde **merak** yüzünden tıklanır; bu artış
zamanla söner. Buna **yenilik etkisi** (novelty effect) denir. Tersi de
olur: alışkanlıklarını bozan bir değişikliğe kullanıcılar önce direnir,
sonra alışır (**öğrenme etkisi**, primacy). Bu bölüm, testin ilk günlerinin
uzun vadeli etkiyi nasıl yanlış gösterebildiğini ölçüyor.

## Gün gün etki

28 gün süren bir testte kullanıcıların günlük tıklamalarını izliyoruz.
Veriyi biz ürettik: B'nin kalıcı etkisi %4. Eski tasarımı bilen
kullanıcılarda buna bir yenilik bonusu ekleniyor: ilk gün %20, her üç
günde yarıya iniyor. Tasarımı hiç görmemiş yeni kullanıcılarda (%20) bonus
yok.

```python
import numpy as np
from ab_data import make_novelty_test

clicks = make_novelty_test()
daily = clicks.groupby(["day", "group"])["clicks"].mean().unstack()
lift = daily["B"] / daily["A"] - 1
print(lift.iloc[[0, 2, 6, 13, 20, 27]].round(3).to_string())
```

```text
day
1     0.190
3     0.153
7     0.100
14    0.059
21    0.054
28    0.058
```

İlk gün B %19,0 önde; dördüncü haftada artış %5,8
civarına iniyor. Hiçbir şey bozulmadı: kullanıcılar yeniliğe alıştı.

## Bir haftalık test ne derdi?

```python
clicks["week"] = (clicks["day"] - 1) // 7 + 1
weekly = clicks.groupby(["week", "group"])["clicks"].mean().unstack()
print((weekly["B"] / weekly["A"] - 1).round(3).to_string())
```

```text
week
1    0.136
2    0.066
3    0.048
4    0.052
```

Yalnızca ilk haftaya bakan bir test etkiyi %13,6 diye raporlardı;
kalıcı etki %4. Ürün kararı, yatırım hesabı ve beklenen gelir bu sayının
üzerine kurulursa üç kat iyimser olur. Tek bir veri setine bağlanmamak için
aynı testi 20 farklı tohumla kuralım:

```python
first, last = [], []
for s in range(100, 120):
    t = make_novelty_test(n=10000, seed=s)
    t["week"] = (t["day"] - 1) // 7 + 1
    w = t.groupby(["week", "group"])["clicks"].mean().unstack()
    lift_w = w["B"] / w["A"] - 1
    first.append(lift_w[1])
    last.append(lift_w[4])
print(round(float(np.mean(first)), 3), round(float(np.mean(last)), 3))
```

```text
0.122 0.037
```

İlk hafta ortalamada %12,2, dördüncü hafta %3,7:
fark tesadüf değil, tasarımın kendisinden geliyor.

## Yeni kullanıcılar: yeniliği görmeyenler

Eski tasarımı hiç görmemiş biri için B "yeni" değildir; sadece tasarımdır.
Bu yüzden yeni kullanıcıların etkisi baştan kalıcı etkiye yakındır:

```python
for new, part in clicks.groupby("is_new"):
    w = part.groupby(["week", "group"])["clicks"].mean().unstack()
    print(new, (w["B"] / w["A"] - 1).round(3).tolist())
```

```text
False [0.16, 0.073, 0.047, 0.053]
True [0.04, 0.038, 0.054, 0.047]
```

Eski kullanıcılarda (`False`) ilk hafta %16,0, yeni
kullanıcılarda (`True`) %4,0. Yeni kullanıcıların ilk haftası,
eski kullanıcıların son haftasına benziyor. İki grubun eğrisi birleşiyorsa
yenilik etkisi vardır; yeni kullanıcı eğrisi kalıcı etkinin erken bir
tahminidir. (Yeni kullanıcılar daha az olduğu için onların sayıları daha
gürültülüdür.)

## Ne yapılır?

- **Testi yeterince uzun tut:** en az iki tam hafta; etki eğrisi
  düzleşene kadar.
- **Etkiyi zamana göre çiz:** gün ya da hafta başına artış. Düşen bir eğri
  yenilik, yükselen bir eğri öğrenme etkisidir.
- **Yeni ve eski kullanıcıyı ayır:** yeni kullanıcı kohortu yenilikten
  arınmış bir bakış verir.
- **Uzun vadeli tutma grubu (holdout):** değişiklik herkese açıldıktan sonra
  küçük bir grup (ör. %5) aylarca eski hâlde bırakılır; kalıcı etki ona
  göre ölçülür.

Erken durmanın burada ayrı bir bedeli var: Sıralı Bakma Tuzağı ve Ardışık
Test bölümündeki kurallarla erken duran bir test, yenilik henüz sönmeden
durabilir.

## Özet

- Yenilik etkisi ilk günlerde etkiyi büyütür, sonra söner; öğrenme etkisi
  tersini yapar.
- Bir haftalık test, bu bölümün verisinde kalıcı etkiyi üç kat abartıyor.
- Etkiyi zamana göre çizmek ve yeni kullanıcıları ayrı okumak iki etkiyi de
  görünür yapar.
- Kalıcı etki için uzun test ya da tutma grubu gerekir.
