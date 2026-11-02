# Riski Değerlendirmek

Bir önceki bölümde riskin "olasılık × etki" olduğunu söyledik. Bu bölümde
o çarpımı gerçekten yapıyoruz. Neden gerekli? Çünkü hiçbir kurumun parası,
zamanı ve insanı her riske yetmez. **Risk değerlendirmesi** (risk
assessment), riskleri karşılaştırılabilir hâle getirip hangisine önce ve
ne kadar emek harcanacağına karar vermektir.

İki yol var: kelimelerle ve küçük puanlarla yapılan **nitel** (qualitative)
değerlendirme ve parayla yapılan **nicel** (quantitative) değerlendirme.
İkisini de göreceğiz.

## Nitel değerlendirme: 1'den 5'e

En yaygın yöntem, olasılığa ve etkiye 1 ile 5 arasında bir puan vermektir.
Puanların ne demek olduğu önceden yazılır, yoksa herkes farklı anlar:

| Puan | Olasılık (likelihood) | Etki (impact) |
|---|---|---|
| 1 | Neredeyse hiç | Önemsiz, kimse fark etmez |
| 2 | Düşük, birkaç yılda bir | Küçük, birkaç saatte düzelir |
| 3 | Orta, yılda bir | Orta, bir gün iş durur |
| 4 | Yüksek, ayda bir | Büyük, müşteri verisi etkilenir |
| 5 | Neredeyse kesin | Çok büyük, kurumun varlığı tehlikede |

**Risk puanı** iki puanın çarpımıdır, yani 1 ile 25 arasında bir sayı.
Bu derste puanı dört **düzeye** ayırıyoruz: 1–4 düşük (L), 5–9 orta (M),
10–16 yüksek (H), 17–25 kritik (C). Kurumlar kendi sınırlarını seçer;
önemli olan sınırın önceden yazılı olmasıdır.

Bütün olası çarpımları bir tabloda görmek, yani bir **risk matrisi** (risk
matrix) çizmek, düzeyleri ezberlemekten kolaydır:

```python
def level(score):
    if score <= 4:
        return "L"
    if score <= 9:
        return "M"
    if score <= 16:
        return "H"
    return "C"


print("impact:      1  2  3  4  5")
for likelihood in range(5, 0, -1):
    row = [level(likelihood * impact) for impact in range(1, 6)]
    print("likelihood", likelihood, " ", "  ".join(row))
```

```text
impact:      1  2  3  4  5
likelihood 5   M  H  H  C  C
likelihood 4   L  M  H  H  C
likelihood 3   L  M  M  H  H
likelihood 2   L  L  M  M  H
likelihood 1   L  L  L  L  M
```

Sağ üst köşe (olası ve büyük) acil, sol alt köşe (zor ve küçük) bekleyebilir.
Dikkat et: olasılığı 1 ama etkisi 5 olan bir risk "düşük" çıkıyor. Bu tür
riskler (deprem, bütün verinin silinmesi) puanla değil ayrıca ele alınır;
sigorta ve felaket kurtarma planı bunun içindir.

Nitel yöntemin iyi yanı hızlı olması; kötü yanı öznelliği. "4 mü 3 mü?"
tartışması sık yaşanır. Puanları tek kişi değil, birkaç kişi birlikte verir.

## Nicel değerlendirme: parayla

Bazen yönetim "bu önlem paramıza değer mi?" diye sorar. O zaman risk para
birimiyle hesaplanır. Üç terim:

- **Varlık değeri** (asset value, AV): varlığın değeri.
- **Maruz kalma oranı** (exposure factor, EF): bir olayda değerin ne
  kadarı kaybolur; 0 ile 1 arasında.
- **Tek kayıp beklentisi** (single loss expectancy, SLE): bir olayın
  maliyeti. **SLE = AV × EF**.
- **Yıllık gerçekleşme oranı** (annual rate of occurrence, ARO): olay
  yılda kaç kez beklenir. On yılda bir ise 0.1.
- **Yıllık kayıp beklentisi** (annual loss expectancy, ALE): bu riskin
  yıllık ortalama maliyeti. **ALE = SLE × ARO**.

Bir örnek: değeri 500 000 olan bir müşteri veritabanı sızarsa değerinin
%40'ı kaybolur (cezalar, müşteri kaybı); böyle bir sızıntı on yılda bir
beklenir.

```python
asset_value = 500_000
exposure = 0.4
aro = 0.1
sle = asset_value * exposure
ale = sle * aro
print(f"SLE: {sle:.0f}  ALE: {ale:.0f}")
```

```text
SLE: 200000  ALE: 20000
```

Bu risk her yıl ortalama 20 000'lik bir kayıp demek. Şimdi yıllık maliyeti
5 000 olan bir önlem düşün; sızıntı olasılığını elli yılda bire (ARO 0.02)
indiriyor. Önlem paraya değer mi?

```python
ale_after = sle * 0.02
cost = 5_000
net = ale - ale_after - cost
print(f"ALE after: {ale_after:.0f}  net benefit: {net:.0f}")
```

```text
ALE after: 4000  net benefit: 11000
```

Önlem riski 20 000'den 4 000'e indiriyor ve kendi maliyetini çıkardıktan
sonra yılda 11 000 kazandırıyor. Net fayda eksi çıksaydı, önlem riskten
pahalı demek olurdu.

Nicel yöntemin zayıf yanı sayılardır: "on yılda bir" çoğu zaman bir
tahmindir. Hesap kesin görünür ama girdisi kadar doğrudur. O yüzden iki
yöntem birlikte kullanılır.

## Riske verilecek dört cevap

Bir risk değerlendirildikten sonra dört şeyden biri yapılır:

| Cevap | Ne demek | Örnek |
|---|---|---|
| **Azaltmak** (mitigate) | Önlem alıp olasılığı ya da etkiyi düşürmek | Parolaya ikinci adım eklemek |
| **Aktarmak** (transfer) | Zararın bir kısmını başkasına devretmek | Siber sigorta, hizmeti uzmanına vermek |
| **Kaçınmak** (avoid) | Riski doğuran işi hiç yapmamak | Gerekmeyen veriyi toplamamak |
| **Kabul etmek** (accept) | Bilerek ve yazılı olarak olduğu gibi bırakmak | Önemsiz bir test sunucusundaki küçük açık |

Hiçbir önlem riski sıfıra indirmez. Önlemlerden sonra kalan riske **artık
risk** (residual risk) denir. Bir kurumun kabul etmeye hazır olduğu risk
miktarına da **risk iştahı** (risk appetite) denir; artık risk bu sınırın
altındaysa kabul edilir.

Kabul etmek "görmezden gelmek" değildir. Kabul edilen risk yazılır, kimin
kabul ettiği not edilir ve belli aralıklarla yeniden bakılır.

## Risk kaydı

Bütün riskler tek bir tabloda tutulur: **risk kaydı** (risk register). Her
satırda riskin adı, olasılığı, etkisi, puanı, sahibi ve verilen cevap
durur. Kayıt en yüksek puandan başlayarak okunur:

```python
register = [("laptop lost", 4, 3), ("db leak", 2, 5),
            ("site down", 3, 3), ("ransomware", 3, 5)]
ranked = sorted(register, key=lambda r: r[1] * r[2], reverse=True)
for name, likelihood, impact in ranked:
    score = likelihood * impact
    print(f"{score:>2} {level(score)} {name}")
```

```text
15 H ransomware
12 H laptop lost
10 H db leak
 9 M site down
```

Fidye yazılımı (3 × 5 = 15) listenin başında. Dizüstü kaybı (12) daha sık
olsa da etkisi daha küçük. Veritabanı sızıntısı ile hizmet kesintisinin
puanları farklı (10 ve 9) ama ikisi de birbirine yakın; böyle durumlarda
puan tek başına karar vermez, ekip konuşur.

## Özet

- Risk değerlendirmesi kıt kaynağı en önemli riske yöneltmek içindir.
- **Nitel:** olasılık ve etki 1–5, puan çarpım, düzeyler önceden yazılı.
- **Nicel:** SLE = AV × EF, ALE = SLE × ARO; önlemin net faydası = önceki
  ALE − sonraki ALE − önlemin maliyeti.
- Dört cevap: **azalt**, **aktar**, **kaçın**, **kabul et**. Kalan risk
  **artık risktir**.
- Riskler **risk kaydında** tutulur ve düzenli olarak yeniden değerlendirilir.
