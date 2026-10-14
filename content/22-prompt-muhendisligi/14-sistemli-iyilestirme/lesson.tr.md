# Promptu Sistemli İyileştirmek

Bir prompt'u iyileştirmenin en yaygın yolu dene-gör: bir cümle ekle, birkaç
mesajla dene, iyi görünüyorsa bırak. Bu yol iki tuzağa düşer. Birincisi,
"iyi görünmek" bir ölçü değil; bir mesajı düzelten değişiklik başka iki
mesajı bozabilir. İkincisi, aynı mesajlara bakarak defalarca düzeltilen
prompt o mesajları ezberler; yeni mesajlarda aynı başarıyı göstermez.

Bu bölümde Promptları Değerlendirmek bölümünde kurduğumuz ölçümü bir
**döngüye** çeviriyoruz: ölç, hataları incele, tek bir değişiklik yap,
yeniden ölç. Ve döngünün en önemli kuralını ölçüyoruz: kararları
**geliştirme kümesiyle** ver, **test kümesine** en sonda bir kez bak.

## Oyuncak model

Döngüyü göstermek için her prompt değişikliğini gerçekten çalıştırabilmemiz
gerekiyor; kayıtlı yanıtlar ise yalnızca yazıldıkları prompt için var. Bu
yüzden bu bölümde bir **oyuncak model** kullanıyoruz. Gerçek bir dil modeli
değil: prompt'taki her kategori satırında listelenen kelimelerden mesajda en
çok geçeni seçiyor, hiçbiri geçmezse `unknown` diyor. Sayılar bu oyuncağın
sayıları; ama yöntem (küme ayırmak, hata incelemek, tek değişiklik,
ezberi yakalamak) gerçek bir modelle aynı.

`shop_data`'daki 40 mesajı ikiye ayırıyoruz: ilk 20'si geliştirme kümesi
(her kategoriden 4), son 20'si test kümesi. Test kümesine bu bölümün
sonuna kadar dokunmuyoruz:

```python
import re

from shop_data import TICKETS


def render(definitions):
    lines = [f"- {label}: {', '.join(words)}"
             for label, words in definitions.items()]
    return "Classify the message into one category.\n" + "\n".join(lines)


def toy_model(prompt, text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    best, best_hits = "unknown", 0
    for label, listed in re.findall(r"^- (\w+): (.+)$", prompt, re.M):
        hits = sum(word in words for word in listed.split(", "))
        if hits > best_hits:
            best, best_hits = label, hits
    return best


def accuracy(prompt, tickets):
    right = sum(toy_model(prompt, t["text"]) == t["label"] for t in tickets)
    return right / len(tickets)


DEV, TEST = TICKETS[:20], TICKETS[20:]
V1 = {"shipping": ["parcel", "delivery", "courier"],
      "returns": ["return", "exchange"],
      "refunds": ["refund", "refunded"],
      "warranty": ["warranty", "broke"],
      "payment": ["pay", "card", "checkout"]}
print(render(V1))
print("v1 dev accuracy", accuracy(render(V1), DEV))
for t in DEV:
    got = toy_model(render(V1), t["text"])
    if got != t["label"]:
        print(f"{t['id']:>2} {t['label']:<8} -> {got:<8} {t['text'][:36]}")
```

```text
Classify the message into one category.
- shipping: parcel, delivery, courier
- returns: return, exchange
- refunds: refund, refunded
- warranty: warranty, broke
- payment: pay, card, checkout
v1 dev accuracy 0.6
 2 returns  -> unknown  How do I send back a jacket that is 
 3 refunds  -> unknown  I returned my order two weeks ago an
 6 shipping -> unknown  The tracking page has not changed fo
 9 warranty -> unknown  A seam of my backpack is coming apar
11 shipping -> unknown  Do you deliver to Switzerland?
14 warranty -> unknown  The sole of my boots came off after 
15 payment  -> unknown  Do you accept bank transfer?
20 payment  -> unknown  I was charged twice for one order.
```

Prompt kategori tanımlarından kuruluyor (`render`); böylece her sürüm bir
sözlük ve iki sürüm arasındaki fark tam olarak görülüyor. İlk sürümün
geliştirme kümesindeki doğruluğu 0,6. Bu **başlangıç ölçüsü** (baseline):
sonraki her değişiklik buna göre değerlendirilecek.

## Hataları incelemek

Hataları tek tek okumadan değişiklik yapmak tahmin etmektir. Burada
sekiz hatanın sekizi de aynı türden: model `unknown` diyor, yani mesajda
tanımlardaki kelimelerin hiçbiri yok. "Yanlış kategori" diye bir hata hiç
yok. Bu bize ne yapacağımızı söylüyor: tanımlar fazla dar. Müşteriler
"delivery" yazmıyor, "deliver" ya da "tracking" yazıyor; "refund" yazmıyor,
"money" yazıyor.

Hataları **türlerine göre** saymak (bilinmeyen, yanlış kategori, biçim
hatası) hangi değişikliğin en çok hatayı çözeceğini gösterir. Önce en
kalabalık türe uğraşılır.

## Genellemek ve ezberlemek

İki yeni sürüm yazalım. `v2`'ye kategorilerin **anlamından** gelen
kelimeler ekleniyor: bir sözcüğün başka biçimleri ve aynı durumu anlatan
yaygın kelimeler. `v3` ise `v2`'nin üstüne geliştirme kümesindeki kalan
hatalardan **doğrudan kopyalanan** kelimeleri ekliyor: "monday",
"switzerland", "boots", "twice"... Bu kelimelerin kategoriyle bir ilgisi
yok; yalnızca o mesajlarda geçiyorlar:

```python
from llm_client import count_tokens

V2 = {"shipping": V1["shipping"] + ["deliver", "delivered", "tracking", "arrived"],
      "returns": V1["returns"] + ["returning", "send", "back"],
      "refunds": V1["refunds"] + ["money"],
      "warranty": V1["warranty"] + ["broken", "stopped", "seam"],
      "payment": V1["payment"] + ["charged", "charge", "transfer"]}
V3 = {"shipping": V2["shipping"] + ["monday", "switzerland", "express"],
      "returns": V2["returns"] + ["small", "boots", "outlet"],
      "refunds": V2["refunds"] + ["returned", "weeks"],
      "warranty": V2["warranty"] + ["sole", "months", "zip"],
      "payment": V2["payment"] + ["twice", "instalments"]}
for name, version in [("v1", V1), ("v2", V2), ("v3", V3)]:
    prompt = render(version)
    dev, test = accuracy(prompt, DEV), accuracy(prompt, TEST)
    print(f"{name}: dev {dev:.2f}  test {test:.2f}  tokens {count_tokens(prompt)}")
```

```text
v1: dev 0.60  test 0.60  tokens 59
v2: dev 0.90  test 0.75  tokens 100
v3: dev 1.00  test 0.75  tokens 139
```

`v2` geliştirme kümesinde 0,60'tan 0,90'a, test kümesinde 0,75'e çıktı:
anlamdan gelen kelimeler yeni mesajlarda da işe yaradı. `v3` geliştirme
kümesinde 1,00'e ulaştı ama test kümesinde `v2` ile aynı kaldı (0,75):
eklenen kelimeler yalnızca o 20 mesajı düzeltti. Geliştirme ile test
arasındaki açık 0,15'ten 0,25'e büyüdü; bu, ezberin (overfitting)
işareti. Üstelik `v3` her çağrıda 139 token, `v2` 100: başarı getirmeyen
39 token her çağrıda ödeniyor. `v2`'nin kendisinde de bir açık var (0,90'a
karşı 0,75), çünkü o da geliştirme kümesinin hatalarına bakılarak yazıldı.
Geliştirme kümesinde ölçülen başarı her zaman biraz iyimserdir; son ölçü
hiç bakılmamış bir kümeden alınır. Burada test kümesine üç sürüm için
baktık, çünkü amaç farkı göstermek; gerçek bir çalışmada yalnızca seçilen
sürüme bakılır.

## Hangi parça işe yarıyor?

Bir prompt büyüdükçe hangi parçasının gerçekten işe yaradığı belirsizleşir.
Bunu ölçmenin yolu **ablasyon** (ablation): her parçayı tek tek çıkarıp
yeniden ölçmek. Çıkarınca başarı düşüyorsa parça işe yarıyor; düşmüyorsa
en azından bu kümede bir katkısı yok. `v2`'ye eklenen kelimeleri tek tek
çıkaralım:

```python
def without(definitions, label, word):
    return {key: [w for w in words if (key, w) != (label, word)]
            for key, words in definitions.items()}


base = accuracy(render(V2), DEV)
useless = []
for label, words in V2.items():
    for word in words:
        if word in V1[label]:
            continue
        change = accuracy(render(without(V2, label, word)), DEV) - base
        if change:
            print(f"without {word:<9} {label:<9} {change:+.2f}")
        else:
            useless.append(word)
print("no effect on dev:", ", ".join(useless))
pair = without(without(V2, "returns", "send"), "returns", "back")
print("without send and back:")
for t in DEV:
    old, new = toy_model(render(V2), t["text"]), toy_model(render(pair), t["text"])
    if old != new:
        print(f"  {t['id']:>2} {t['label']:<8} {old} -> {new}")
```

```text
without deliver   shipping  -0.05
without tracking  shipping  -0.05
without back      returns   +0.05
without seam      warranty  -0.05
without charged   payment   -0.05
without transfer  payment   -0.05
no effect on dev: delivered, arrived, returning, send, money, broken, stopped, charge
without send and back:
   2 returns  returns -> unknown
   3 refunds  returns -> refunds
```

Beş kelimeyi çıkarmak başarıyı 0,05 düşürüyor: her biri bir mesajı tek
başına kurtarıyor. `back`'i çıkarmak ise başarıyı **artırıyor**: 3 numaralı
mesaj ("...no money back") `back` yüzünden para iadesi yerine geri gönderme
sayılıyordu. Sekiz kelimenin bu kümede tek başına hiçbir etkisi yok. Ama
"etkisiz" iki şey demek olabilir: kelime bu 20 mesajda hiç geçmiyor ya da
yanında başka bir kelime aynı işi yapıyor. `send` ile `back`'i birlikte
çıkarınca toplam değişmiyor ama iki mesajın cevabı değişiyor: biri
bozuluyor (2), biri düzeliyor (3). Toplam aynı kalırken cevaplar
değişebilir; bu yüzden değişiklikler mesaj mesaj karşılaştırılır. Küçük
bir kümede "etkisiz" çıkan bir parçayı silmeden önce daha büyük bir
kümeyle ölçmek gerekir.

## Döngü

Bütün bölümü bir çalışma düzenine çevirelim:

1. **Değerlendirme kümesini kur** ve ikiye ayır: geliştirme ve test. İki
   kümede de her kategoriden yeterince örnek olsun.
2. **Başlangıcı ölç** ve kaydet.
3. **Hataları oku** ve türlerine göre say. En kalabalık türden başla.
4. **Tek bir değişiklik yap.** İki değişiklik birlikte yapılırsa hangisinin
   işe yaradığı (ya da hangisinin bir şeyi bozduğu) bilinmez.
5. **Geliştirme kümesinde yeniden ölç.** Yalnızca toplam başarıya değil,
   önceden doğru olan cevaplardan bozulan var mı ona da bak (Promptları
   Değerlendirmek bölümündeki karşılaştırma).
6. **Günlüğe yaz:** sürüm, değişiklik, gerekçe, ölçü. Sistem Mesajı
   bölümündeki sürüm özeti burada işe yarar.
7. Yeterince iyi olunca **test kümesine bir kez bak.** Test sonucuna göre
   prompt'u yeniden düzeltirsen test kümesi artık geliştirme kümesi olur;
   bundan sonra güvenilir ölçü için yeni, hiç bakılmamış mesajlar gerekir.

Küçük kümelerde bir de belirsizlik var: 20 mesajda bir mesaj 5 puan.
0,05'lik bir fark tek bir mesaj demek; Promptları Değerlendirmek
bölümündeki bootstrap aralığı bu yüzden önemli.

## Özet

- Dene-gör yerine döngü: ölç, hataları oku, tek değişiklik, yeniden ölç,
  günlüğe yaz.
- Kararlar geliştirme kümesiyle verilir; test kümesine en sonda bir kez
  bakılır.
- Geliştirme kümesindeki mesajlardan kopyalanan ayrıntılar o kümede başarıyı
  artırır ama yeni mesajlarda artırmaz: ezber. Geliştirme ile test
  arasındaki açık bunu gösterir.
- Hatalar türlerine göre sayılır; en kalabalık türden başlanır.
- Ablasyon hangi parçanın işe yaradığını gösterir; tek tek çıkarınca
  etkisiz görünen parçalar birlikte etkili olabilir ve küçük bir kümede
  "etkisiz" zayıf bir kanıttır.
- Daha uzun prompt her çağrıda daha çok token demek; başarı getirmeyen
  ekleme maliyettir.
