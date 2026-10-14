# RAG'i Değerlendirmek

Önceki bölümde RAG düzeneği bazı soruları doğru cevapladı, bazılarında
yanıldı. "Doğruluk %62" gibi tek bir sayı neyin düzeltileceğini
söylemez: hata aramadan mı geliyor, okumadan mı? Bu bölüm bir RAG
sistemini **parça parça** ölçmeyi gösteriyor: önce getirme, sonra cevap,
sonra çekimser kalma; en sonda da küçük bir değerlendirme kümesinin
sınırları.

## Değerlendirme kümesi

Elimizde 27 soru var. Her birinin cevabını veren makale ve doğru cevapta
geçmesi gereken ifade (`key`) yazılı; üçünün cevabı belgelerde yok. Böyle
bir küme, gerçek kullanıcı sorularından seçilip elle etiketlenerek
kurulur ve sistem her değiştiğinde aynı kümeyle yeniden ölçülür.
10'daki düzenek `rag_tools.py` dosyasında.

## 1. Getirmeyi ölçmek

Cevap ifadesini içeren ilk parçanın sırasına (**rank**) bakıyoruz. İki ölçü:

- **recall@k:** ifadenin ilk `k` parçada bulunduğu soruların oranı.
- **MRR** (mean reciprocal rank): her soru için `1 / sıra` (hiç
  bulunmadıysa 0), sorular üzerinden ortalama. Doğru parça birinci
  sıradaysa 1, ikinciyse 0,5; doğru parçayı üste koyan arama ödüllenir.

```python
from rag_tools import index, rag, NOT_FOUND, QUESTIONS

answerable = [q for q in QUESTIONS if q["doc"]]


def first_rank(question, key, k=10):
    found = index.search(question, k)
    for rank, ((_, text), _) in enumerate(found, 1):
        if key in text:
            return rank
    return None


ranks = [first_rank(q["q"], q["key"]) for q in answerable]
for k in [1, 3, 5, 10]:
    hits = sum(r is not None and r <= k for r in ranks)
    print(f"recall@{k:<2}", round(hits / len(ranks), 2))
print("MRR", round(sum(1 / r for r in ranks if r) / len(ranks), 2))
```

```text
recall@1  0.71
recall@3  0.71
recall@5  0.75
recall@10 0.96
MRR 0.75
```

Doğru cümle soruların %71'inde birinci sırada ve ilk üçte de aynı oran:
birinci sırada çıkmayan, ikinci ya da üçüncüde de çıkmıyor. İlk 10 parçaya
bakınca oran %96'ya çıkıyor; doğru cümle çoğu zaman listede ama aşağılarda.
MRR 0,75.

## 2. Hatanın yerini bulmak

Her yanlış ya da kaçırılan cevabı iki gruptan birine koyalım: doğru
parça ilk üç kaynakta **yoksa** getirme hatası, **varsa** okuma hatası.

```python
table = {"correct": 0, "retrieval miss": 0, "reading error": 0}
for q, rank in zip(answerable, ranks):
    reply = rag(q["q"], 3, 2)
    if q["key"] in reply.text:
        table["correct"] += 1
    elif rank is None or rank > 3:
        table["retrieval miss"] += 1
    else:
        table["reading error"] += 1
print(table)
```

```text
{'correct': 15, 'retrieval miss': 7, 'reading error': 2}
```

Kaçan dokuz cevabın yedisi getirme hatası: doğru cümle ilk üç kaynağın
içinde yok ve okuyucu ne yaparsa yapsın cevabı bulamaz. Yalnızca ikisi okuma
hatası. Demek ki bu sistemde ilk iş aramayı iyileştirmek (09: gömme ya da
karma arama); prompt'la ya da modelle uğraşmak en fazla iki soruyu
kurtarabilir. Tek bir doğruluk sayısı bunu göstermezdi.

## 3. Çekimser kalmayı ölçmek

"Bulamadım" cevabı da bir tahmin: cevabı olmayan soruyu doğru tanımak.
İki soru soruyoruz: "bulamadım" dediğinde ne kadar haklı (**kesinlik**) ve
cevabı olmayan soruların ne kadarını tanıyor (**duyarlılık**)?

```python
for min_overlap in [1, 2, 3]:
    said = right = 0
    for q in QUESTIONS:
        if rag(q["q"], 3, min_overlap).text == NOT_FOUND:
            said += 1
            right += q["key"] is None
    unanswerable = sum(q["key"] is None for q in QUESTIONS)
    print(f"overlap>={min_overlap} said not found {said:2}",
          f"precision {right / said:.2f} recall {right / unanswerable:.2f}")
```

```text
overlap>=1 said not found  3 precision 0.33 recall 0.33
overlap>=2 said not found 10 precision 0.30 recall 1.00
overlap>=3 said not found 25 precision 0.12 recall 1.00
```

Eşik 2'de cevabı olmayan üç sorunun üçü de tanınıyor (duyarlılık 1,00),
ama "bulamadım" cevaplarının yalnızca %30'u gerçekten cevapsız sorulara
gidiyor; geri kalan yedisi cevabı olan sorular. Eşik 3'te 27 sorunun 25'ine
"bulamadım" deniyor: duyarlılık yine 1,00, ama sistem neredeyse hiçbir
şeye cevap vermiyor ve kesinlik 0,12'ye düşüyor. Eşik 1'de yalnızca üç kez
"bulamadım" deniyor ve bunların biri doğru. Yalnızca duyarlılığa bakan biri,
her şeye "bulamadım" diyen bir sistemi mükemmel sanabilir; iki ölçü birlikte
okunur.

## 4. Küçük kümenin sınırı

24 cevaplanabilir soruda **bir** soru 4,2 puan eder. 10'da eşik 1, eşik
2'den iki soru fazla doğru cevap vermişti (17'ye 15). Bu fark güvenilir mi?
Soruları **yeniden örnekleyerek** (bootstrap) bakalım: 24 soruyu yerine
koyarak 24 kez çekip iki ayarın doğru sayısı farkını 2000 kez
hesaplıyoruz. Farkın dağılımı, başka bir 24 soruluk kümede ne
görebileceğimiz hakkında bir fikir verir.

```python
import numpy as np


def correct_vector(min_overlap):
    return np.array([q["key"] in rag(q["q"], 3, min_overlap).text
                     for q in answerable])


a, b = correct_vector(1), correct_vector(2)
print("overlap>=1", a.sum(), "overlap>=2", b.sum())
rng = np.random.default_rng(0)
diffs = []
for _ in range(2000):
    pick = rng.integers(0, len(a), len(a))
    diffs.append(a[pick].sum() - b[pick].sum())
low, high = np.percentile(diffs, [5, 95])
print("difference", a.sum() - b.sum(), "90% interval", low, high)
print("share of resamples with no gain", np.mean(np.array(diffs) <= 0))
```

```text
overlap>=1 17 overlap>=2 15
difference 2 90% interval 0.0 4.0
share of resamples with no gain 0.1105
```

Fark 2 soru; ama farkın %90 aralığı 0 ile 4 arasında ve yeniden
örneklemelerin %11'inde eşik 1 hiç kazanç sağlamıyor. Bu kadar küçük bir
kümede iki soruluk farka dayanarak karar vermek güvenli değil. Üstelik eşik
1, 10'da 5 yanlış cevap fazla veriyordu (7'ye 2). Tek bir sayı yerine bütün
tabloya bakılır ve karar önemliyse küme büyütülür.

## Serbest cevapları değerlendirmek

Bu bölümde cevabın doğruluğunu bir ifadenin geçip geçmemesiyle ölçtük;
örnek okuyucu kaynağın cümlesini aynen döndürdüğü için bu yetti. Gerçek
bir model aynı bilgiyi kendi cümleleriyle yazar ("üç yıl geçerli" yerine
"üç yıl sonra sona erer"); o zaman ifade eşleşmesi doğru cevabı da yanlış
sayabilir. Pratikte üç yol birlikte kullanılır:

- **İnsan değerlendirmesi:** küçük bir örneklemde en güvenilir ölçü.
- **Kurallı denetim:** sayılar, tarihler, adlar kaynakta geçiyor mu (08).
- **Model ile değerlendirme:** başka bir modelden, cevabı kaynakla ve
  doğru cevapla karşılaştırıp puanlamasını istemek. Hızlıdır ama o modelin
  de hataları vardır; puanları birkaç örnekte insan değerlendirmesiyle
  karşılaştırılır.

## Özet

- RAG parça parça ölçülür: getirme (recall@k, MRR), cevap (doğru, yanlış,
  kaçırılan), çekimser kalma (kesinlik, duyarlılık).
- Hatanın yeri ayrılınca neyin düzeltileceği belli olur: getirme hatasına
  arama, okuma hatasına prompt ya da model.
- Küçük bir kümede birkaç sorunun farkı anlamlı olmayabilir; karar için
  daha çok soru gerekir.
- Değerlendirme kümesi sabit tutulur; sistem her değişince aynı kümeyle
  yeniden ölçülür.
