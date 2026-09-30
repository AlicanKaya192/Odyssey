## Üç birleştirme türü

| Araç | Eşleştirme | Ne zaman |
|---|---|---|
| `merge` | Anahtar **birebir** aynı | Aynı sıklıkta iki tablo; ay ve mağaza gibi anahtarlar |
| `merge_asof` | **En yakın** önceki (ya da sonraki) kayıt | Fiyat listesi, kur, ayar değişikliği, farklı saatlerde gelen ölçümler |
| `join` / `concat(axis=1)` | İndekse göre hizalama | Aynı indeksli seriler yan yana |

## `merge_asof`

```python
pd.merge_asof(left, right, on="date")                    # ayni adli tarih sutunu
pd.merge_asof(left, right, left_on="date", right_on="valid_from")
pd.merge_asof(left, right, on="date", by="store")        # seri bazinda
pd.merge_asof(left, right, on="time", tolerance=pd.Timedelta("10min"))
pd.merge_asof(left, right, on="time", direction="nearest")
```

| Parametre | Ne yapıyor |
|---|---|
| `direction="backward"` | O tarihte ya da **önceki** en son kayıt (varsayılan) |
| `direction="forward"` | O tarihte ya da **sonraki** ilk kayıt; geleceği kullanır |
| `direction="nearest"` | Hangi yönde yakınsa; geleceği kullanabilir |
| `tolerance=` | Bundan uzak kayıt eşleşmesin; `NaN` kalsın |
| `by=` | Eşleştirmeyi bu sütunun değerine göre ayrı ayrı yap |
| `allow_exact_matches=False` | Tam aynı anı eşleme; kesinlikle önceki |

**İki tablo da anahtar sütuna göre sıralı olmalı.** Değilse
`left keys must be sorted` hatası.

**Tahmin için `backward`.** `forward` ve `nearest` bir satıra kendisinden
sonra gelen bir kaydı getirebiliyor; analizde sorun değil, özellik kurarken
sızıntı.

**`tolerance` eski veriyi engelliyor.** Sensör iki gündür kayıt göndermediyse
`merge_asof` yine de iki gün önceki değeri getiriyor. `tolerance` ile "bundan
eskisi geçersiz" diyebiliyorsun.

**`allow_exact_matches=False`** olayla aynı anda gelen kaydın kullanılmasını
engelliyor. Günlük veride "bugünün fiyatı bugünün satışından önce mi
biliniyordu?" sorusunun cevabı hayırsa bunu kullan.

## Farklı sıklıklar

| Durum | Yol |
|---|---|
| Günlük satış + aylık hedef | Günlüğü aya **indir**, sonra `merge` |
| Günlük satış + aylık fiyat listesi (seviye) | Fiyatı günlere **taşı**: `merge_asof` ya da `ffill` |
| Saatlik tüketim + günlük sıcaklık | Ya tüketimi güne indir ya sıcaklığı saatlere taşı (bilerek) |
| İki düzensiz sensör | İkisini de aynı ızgaraya `resample`, sonra birleştir |

Genel kural Bölüm 05'ten: **toplam aşağı iner, seviye yukarı taşınır.**

## Aynı dönemi eşlemek

Aylık tabloları birleştirirken etiket farkına dikkat:

```python
a.index = a.index.to_period("M")     # 2024-03-31 -> 2024-03
b.index = b.index.to_period("M")     # 2024-03-01 -> 2024-03
a.to_frame("a").join(b.to_frame("b"))
```

Biri ay sonu, öteki ay başıyla etiketlenmiş iki tabloyu doğrudan birleştirmek
hiçbir satırı eşlemiyor. İkisini de periyoda çevirmek en sağlam yol.

## Birleştirmeden sonra kontrol

```python
print(len(left), len(joined))                 # satir sayisi degisti mi?
print(joined["price"].isna().sum())           # eslesmeyen kac satir var?
print(joined["date"].duplicated().sum())      # satirlar cogaldi mi?
```

- **Satır sayısı arttıysa** sağ tabloda anahtar tekrar ediyor; her sol satır
  birden çok kez eşleşmiş ve toplamlar şişmiş.
- **`NaN` çoksa** anahtarlar tutmuyor: tür farkı (metin ve tarih), etiket
  farkı (ay başı ve ay sonu), boşluk ya da büyük-küçük harf.
- `merge(..., validate="many_to_one")` beklediğin ilişkiyi denetletiyor; sağ
  tarafta tekrar varsa hata veriyor.

## Seriler arası gecikmeli ilişki

Bir serinin başka bir seriyi **önceden** haber verip vermediğine bakmak için
birini kaydırıp korelasyona bak:

```python
for k in (0, 1, 7):
    print(k, round(wide["A"].corr(wide["B"].shift(k)), 3))
```

Buna çapraz korelasyon deniyor. Yüksek bir değer nedensellik kanıtı değil:
iki seri de aynı takvimi (hafta sonu, tatil) izliyor olabilir. Bölüm 18'de
dışsal değişkenlerle birlikte ele alacağız.
