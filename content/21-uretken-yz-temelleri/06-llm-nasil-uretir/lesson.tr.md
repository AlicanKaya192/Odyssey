# Büyük Dil Modeli Nasıl Üretir

Buraya kadar resim ve nokta üreten modeller gördük. Modülün geri kalanı
metin üreten **büyük dil modelleri** (large language models, **LLM**)
üzerine. NLP patikasının Gömmeler ve Dil Modelleri modülünde temelleri
kurduk: transformer, ön eğitim ve kod çözme (açgözlü seçim, sıcaklık, en
olası k, çekirdek örnekleme). Bu bölüm o parçaları bir **sohbet modeline**
bağlıyor: bir mesaj listesi nasıl tek bir metne dönüşür, model cevabı
nerede bitirir ve neden bilmediği bir soruya da akıcı bir cevap verir.

## Model yalnızca devam ettirir

Bir dil modelinin tek yeteneği, verilen metnin **sıradaki token'ını**
tahmin etmektir. Soru sormak, cevap almak, rol yapmak; hepsi bu tek işin
üstüne kurulur. Sohbet modelleri, eğitim verisi belli bir **sohbet
şablonuyla** (chat template) yazılmış diyaloglardan oluştuğu için bir
soruya "cevap verir gibi" devam ederler.

Bunu küçük bir oyuncak modelle görelim. On ülkenin başkentini üç farklı
soru kalıbıyla soran 30 diyalog yazıyoruz. Her mesaj, rolünü gösteren bir
işaretle (`<user>`, `<assistant>`) tek bir token dizisine ekleniyor ve
cevap `<end>` işaretiyle bitiyor:

```python
import numpy as np
from collections import Counter

CAPITALS = {"france": "paris", "germany": "berlin", "italy": "rome",
            "spain": "madrid", "japan": "tokyo", "egypt": "cairo",
            "canada": "ottawa", "kenya": "nairobi", "peru": "lima",
            "norway": "oslo", "turkey": "ankara", "chile": "santiago"}
KNOWN = list(CAPITALS)[:10]
QUESTIONS = ["what is the capital of {c} ?",
             "which city is the capital of {c} ?",
             "tell me the capital of {c} ."]


def render_chat(messages):
    tokens = []
    for m in messages:
        tokens += ["<" + m["role"] + ">"] + m["content"].split()
    return tokens + ["<assistant>"]


dialogues = []
for c in KNOWN:
    for q in QUESTIONS:
        msgs = [{"role": "user", "content": q.format(c=c)}]
        answer = f"the capital of {c} is {CAPITALS[c]} . <end>"
        dialogues.append(render_chat(msgs) + answer.split())
print(len(dialogues))
print(" ".join(dialogues[0]))
```

```text
30
<user> what is the capital of france ? <assistant> the capital of france is paris . <end>
```

`render_chat` bir sohbet API'sinin arka planda yaptığı işin küçük bir
benzeri: mesaj listesini rol işaretleriyle tek diziye çeviriyor ve en
sona `<assistant>` ekleyerek "şimdi sıra asistanda" diyor. Gerçek
modellerin işaretleri farklıdır ama fikir aynı. Türkiye ve Şili
sözlükte var, ama eğitim diyaloglarında **yok**: model bu iki ülkeyi hiç
görmeyecek.

## Oyuncak model: en uzun eşleşen bağlam

Gerçek bir LLM'de sıradaki token'ı bir transformer tahmin eder. Biz
sayarak tahmin eden bir model kuruyoruz: her konumda, önceki 1–7 token'ı
bağlam olarak alıp ardından gelen token'ı sayıyoruz. Tahmin ederken
**en uzun** tanıdık bağlamı kullanıyoruz; tanıdık değilse bir kısaltıp
yeniden deniyoruz (NLP patikasındaki n-gram modelinin geri çekilmeli,
değişken uzunluklu hâli).

```python
ORDER = 8
tables = [dict() for _ in range(ORDER)]
for d in dialogues:
    for i in range(1, len(d)):
        for n in range(1, min(i, ORDER - 1) + 1):
            context = tuple(d[i - n:i])
            tables[n].setdefault(context, Counter())[d[i]] += 1


def next_probs(context):
    for n in range(ORDER - 1, 0, -1):
        counts = tables[n].get(tuple(context[-n:]))
        if counts:
            break
    words = sorted(counts)
    p = np.array([counts[w] for w in words], dtype=float)
    return words, p / p.sum()


words, p = next_probs("capital of france is".split())
print(words, p)
words, p = next_probs(["of"])
print(len(words), "choices after 'of'")
```

```text
['paris'] [1.]
10 choices after 'of'
```

"capital of france is" bağlamından sonra tek seçenek var: `paris`. Tek
başına "of"tan sonra ise on ülkenin hepsi mümkün; hangisinin geleceğini
ancak daha uzun bağlam söyler.

## Üretim döngüsü ve bitiş nedeni

Cevap token token üretiliyor: dağılımı al, bir token seç, diziye ekle,
yeniden. Döngüyü iki şey durdurur:

- Model **durma işaretini** (`<end>`) üretir: cevap bitmiştir. Bitiş
  nedeni (finish reason) `stop`.
- Üretilen token sayısı **`max_tokens`** sınırına ulaşır: cevap yarıda
  kesilir. Bitiş nedeni `length`.

Sohbet API'leri bu bilgiyi cevapla birlikte döndürür. `length` gören bir
program cevabın eksik olduğunu bilmelidir.

```python
def generate(messages, max_tokens=20, temperature=0.0, seed=0):
    rng = np.random.default_rng(seed)
    tokens = render_chat(messages)
    out = []
    while len(out) < max_tokens:
        words, p = next_probs(tokens + out)
        if temperature == 0:
            w = words[int(np.argmax(p))]
        else:
            q = p ** (1 / temperature)
            w = words[rng.choice(len(words), p=q / q.sum())]
        if w == "<end>":
            return " ".join(out), "stop"
        out.append(w)
    return " ".join(out), "length"


def ask(country, **kwargs):
    msg = {"role": "user", "content": f"what is the capital of {country} ?"}
    return generate([msg], **kwargs)


for c in ["france", "japan"]:
    print(ask(c))
print(ask("france", max_tokens=3))
```

```text
('the capital of france is paris .', 'stop')
('the capital of japan is tokyo .', 'stop')
('the capital of', 'length')
```

Sıcaklık 0 iken her adımda en olası token seçiliyor (açgözlü seçim); bu
yüzden cevap her çalıştırmada aynı. `max_tokens=3` ile cevap üçüncü
token'da kesildi ve bitiş nedeni `length`.

## Şablon neden önemli?

`<assistant>` işaretini koymadan, yalnızca kullanıcının sorusunu verirsek
model ne yapar?

```python
user_only = ["<user>"] + "what is the capital of france ?".split()
print(next_probs(user_only))
```

```text
(['<assistant>'], array([1.]))
```

Model sıradaki token olarak `<assistant>` işaretini kendisi yazmak
istiyor: o bir cevap değil, diyaloğun devamı. Model "soruya cevap
vermiyor", eğitim verisindeki **metne benzeyen** bir devam üretiyor. Şablonu
doğru kurmak bu yüzden önemli; sohbet API'leri şablonu senin yerine
kuruyor, sen yalnızca mesaj listesini veriyorsun.

## Bilmediği soruya da cevap verir

Şimdi eğitim diyaloglarında olmayan iki ülkeyi soralım:

```python
for c in ["turkey", "chile"]:
    print(c, ask(c))
answers = Counter(ask("chile", temperature=1.0, seed=s)[0]
                  for s in range(200))
print(len(answers), "different answers in 200 tries")
for text, n in answers.most_common(3):
    print(n, text)
```

```text
turkey ('the capital of canada is ottawa .', 'stop')
chile ('the capital of canada is ottawa .', 'stop')
10 different answers in 200 tries
26 the capital of germany is berlin .
26 the capital of kenya is nairobi .
24 the capital of france is paris .
```

Model "bilmiyorum" demiyor; dilbilgisi kusursuz, kendinden emin ama
**başka bir sorunun cevabı** olan bir cümle kuruyor. Sıcaklık 1'de 200
denemede 10 farklı cevap çıkıyor ve hiçbiri Şili'nin başkenti
değil: model yalnızca gördüğü cümle parçalarını birleştirebiliyor.
Gerçek LLM'ler çok daha büyük ve çok daha fazla şey "biliyor", ama ilke
aynı: model, verisinde dayanağı olmayan bir soruya da akıcı bir metin
üretir. Bu davranışa **halüsinasyon** denir ve iki bölüm sonra ayrıntısıyla
konusu olacak.

## Sıcaklık ne zaman bir şey değiştirir?

Aynı soruyu farklı sıcaklıklarla 50 kez soralım ve kaç farklı cevap
çıktığını sayalım; bir kez bildiği, bir kez bilmediği ülke için:

```python
for country in ["france", "chile"]:
    for t in [0.0, 0.7, 1.5]:
        outs = {ask(country, temperature=t, seed=s)[0] for s in range(50)}
        print(country, "temperature", t, "->", len(outs), "answers")
```

```text
france temperature 0.0 -> 1 answers
france temperature 0.7 -> 1 answers
france temperature 1.5 -> 1 answers
chile temperature 0.0 -> 1 answers
chile temperature 0.7 -> 10 answers
chile temperature 1.5 -> 10 answers
```

Bildiği soruda sıcaklık hiçbir şey değiştirmiyor: dağılımın tek bir
seçeneği var. Bilmediği soruda sıcaklık 0 tek, kararlı bir cevap veriyor
(ama yanlış); sıcaklık artınca 50 denemede 10 farklı cevap çıkıyor. Gerçek
modellerde de aynı: aynı soruyu birkaç kez sorup cevapların tutarlı olup
olmadığına bakmak, modelin o konuda ne kadar dayanağı olduğuna dair bir
ipucudur. Sıcaklığı 0 yapmak cevabı tekrarlanabilir yapar, **doğru**
yapmaz.

## Model hatırlamaz

Sohbet API'leri **durumsuzdur** (stateless): model önceki çağrıları
hatırlamaz. "Az önce ne dedin?" sorusunun cevabını verebilmesi için
önceki mesajların hepsinin, her çağrıda yeniden gönderilmesi gerekir.
Sohbet uygulamalarının "belleği", aslında program tarafından tutulan ve
her seferinde baştan gönderilen mesaj listesidir. Bunun bir bedeli var:
liste uzadıkça her çağrıda daha çok token işlenir. Sonraki bölümün konusu
bu.

## Özet

- Bir LLM'in tek işi sıradaki token'ı tahmin etmek; sohbet, bu işin
  üstüne kurulmuş bir şablondur.
- Mesaj listesi rol işaretleriyle tek bir diziye çevrilir; sona eklenen
  asistan işareti "sıra sende" der.
- Üretim, durma işareti (`stop`) ya da `max_tokens` sınırıyla (`length`)
  biter; `length` cevabın eksik olduğunu söyler.
- Model bilmediği soruya da akıcı bir cevap üretir (oyuncak modelde 200
  denemede hiç doğru cevap yok).
- Sıcaklık 0 cevabı tekrarlanabilir yapar, doğru yapmaz; tutarsız cevaplar
  dayanağın zayıf olduğuna işarettir.
- API durumsuzdur: geçmiş her çağrıda yeniden gönderilir.
