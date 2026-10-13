# Tokenizasyon

Bir modelin metinle çalışabilmesi için önce metni parçalara ayırmak gerekir.
Bu parçalara **token**, ayırma işine **tokenizasyon** (tokenisation)
deniyor. Şimdiye kadar `split()` kullandık; bu bölüm `split()`'in nerede
yetmediğini, düzenli ifadelerle (regular expression) kendi parçalayıcımızı
yazmayı, scikit-learn'ün varsayılan parçalayıcısının sessizce neleri attığını
ve metni cümlelere bölmenin neden sanıldığı kadar kolay olmadığını
anlatıyor.

## split() neden yetmiyor?

Bir destek talebinden alınmış gibi bir cümle:

```python
text = "I can't wait: $49.99 for ORD-48213?! Mail ana12@example.com."
print("|".join(text.split()))
```

```text
I|can't|wait:|$49.99|for|ORD-48213?!|Mail|ana12@example.com.
```

`split()` yalnızca boşluklardan bölüyor; `|` işareti parçaların sınırını
gösteriyor. Sorunlar:

- **Noktalama kelimeye yapışıyor:** "wait:" ve "ORD-48213?!" birer token.
  "wait" kelimesi metinde "wait", "wait:" ve "wait." olarak geçerse üç ayrı
  token olur.
- **E-posta noktasıyla birlikte:** "ana12@example.com." sonundaki nokta
  cümlenin noktası, adresin parçası değil.

## Düzenli ifadeyle parçalamak

İlk deneme: harf ve rakam dizilerini (`\w+`) ve boşluk olmayan her tek
işareti (`[^\w\s]`) ayrı token yap.

```python
import re

print("|".join(re.findall(r"\w+|[^\w\s]", text)))
```

```text
I|can|'|t|wait|:|$|49|.|99|for|ORD|-|48213|?|!|Mail|ana12|@|example|.|com|.
```

- `\w` harf, rakam ve alt çizgi; `\s` her türlü boşluk. `[^\w\s]` ikisi de
  olmayan, yani noktalama.
- `re.findall` desene uyan bütün parçaları sırayla döndürüyor. `|` desende
  "ya o ya bu" demek.
- Noktalama artık ayrı, ama bu kez fazla parçalandı: "can't" üç token
  (`can`, `'`, `t`), "$49.99" dört token, sipariş numarası ve e-posta
  dağıldı. Tutar 49,99 dolar bilgisi artık hiçbir token'da yok.

## Kendi desenini yazmak

Çözüm: önemli kalıpları önce, genel kuralı sona yazmak. `re.findall`
alternatifleri soldan sağa dener ve ilk uyanı alır.

```python
import re

TOKEN = re.compile(r"""
    [\w.+-]+@\w+\.\w+      # e-posta
  | \$\d+(?:\.\d+)?        # para
  | [A-Z]+-\d+             # sipariş numarası
  | \w+(?:'\w+)?           # kelime; can't tek parça
  | [^\w\s]                # tek bir noktalama işareti
""", re.VERBOSE)

print("|".join(TOKEN.findall(text)))
```

```text
I|can't|wait|:|$49.99|for|ORD-48213|?|!|Mail|ana12@example.com|.
```

- `re.VERBOSE` desene boşluk ve `#` ile açıklama yazmaya izin veriyor; uzun
  desenler böyle okunur hâle gelir.
- `(?:...)` gruplar ama ayrı yakalamaz; `findall`'ın tam eşleşmeyi döndürmesi
  için gerekli.
- `\w+(?:'\w+)?` kelimeyi, varsa kesme işaretli devamıyla birlikte alıyor:
  "can't", "it's", "I'm" tek token.
- **Sıra önemli:** kelime kuralı başta olsaydı "ana12" e-posta kuralından
  önce yakalanır, e-posta yine dağılırdı.

Her görev kendi desenini ister. Destek taleplerinde sipariş numarası ve tutar
önemli; tweet'lerde `#etiket` ve `@kullanıcı`; kodda `snake_case` ve
`a.b()`.

## scikit-learn'ün varsayılan parçalayıcısı

İleride metni sayıya çevirmek için `CountVectorizer` ve `TfidfVectorizer`
kullanacağız. İkisinin de içinde bir parçalayıcı var ve **sessizce** bazı
şeyleri atıyor:

```python
from sklearn.feature_extraction.text import CountVectorizer

analyze = CountVectorizer().build_analyzer()
print(analyze("I can't wait: it's a 5-star deal!"))
```

```text
['can', 'wait', 'it', 'star', 'deal']
```

- `build_analyzer()` vektörleştiricinin metni nasıl parçaladığını
  gösteriyor: önce küçük harfe çeviriyor, sonra `token_pattern` ile
  parçalıyor.
- Varsayılan desen `r"(?u)\b\w\w+\b"`: **en az iki karakterlik** kelimeler.
  "I", "a", "5" atıldı; "can't" "can" oldu, "t" düştü; "it's" "it" oldu.
- Yani olumsuzlamanın izi ("n't") kayboldu: "can" ile "can't" aynı token.
  Duygu analizinde bu ciddi bir kayıp. `CountVectorizer(token_pattern=...)`
  ya da `tokenizer=` ile kendi parçalayıcını verebilirsin.

## Hangi parçalayıcı kaç token üretiyor?

2000 destek talebinde dört parçalayıcıyı karşılaştıralım. Hepsi küçük harfle
çalışsın ki fark yalnızca parçalamadan gelsin.

```python
import re
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
analyze = CountVectorizer().build_analyzer()
tokenizers = {
    "split": lambda t: t.lower().split(),
    "regex": lambda t: re.findall(r"\w+|[^\w\s]", t.lower()),
    "pattern": lambda t: [tok.lower() for tok in TOKEN.findall(t)],
    "sklearn": analyze,
}
for name, tokenize in tokenizers.items():
    tokens = [tok for t in texts for tok in tokenize(t)]
    print(name, len(tokens), len(set(tokens)))
```

```text
split 36829 1718
regex 47205 1497
pattern 43840 1572
sklearn 35699 1479
```

İlk sayı toplam token, ikinci sayı farklı token (kelime dağarcığı).

- **split** en büyük dağarcığı veriyor: noktalama yapıştığı için "order",
  "order." ve "order?" ayrı sayılıyor.
- **regex** en çok token'ı üretiyor (her noktalama ayrı, sipariş numarası
  üç parça) ama dağarcığı küçük; rakam parçaları ortak.
- **pattern** e-postaları, tutarları ve sipariş numaralarını bütün tuttuğu
  için dağarcığı regex'ten büyük: "ana12@example.com" ve "$49.99" gibi her
  biri ayrı bir "kelime". Bu token'lar çoğu zaman tek bir talepte geçiyor,
  model için faydasız. Çözüm onları `<email>`, `<money>` gibi yer
  tutuculara çevirmek; 03. ve 14. bölümlerde.
- **sklearn** en az token'ı üretiyor: noktalama ve tek harfler yok.

Doğru parçalayıcı yok; görevine uyan parçalayıcı var. Önemli olan neyin
atıldığını **bilmek**.

## Cümlelere bölmek

Özetleme ya da çeviri gibi görevler metni önce cümlelere ayırır. İlk akla
gelen: nokta, ünlem ya da soru işaretinden sonra gelen boşluktan böl.

```python
import re


def sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


for s in sentences("Dr. Lee paid $4.50 today. Great service! Would buy again."):
    print(repr(s))
```

```text
'Dr.'
'Lee paid $4.50 today.'
'Great service!'
'Would buy again.'
```

- `(?<=[.!?])` "geriye bakış" (lookbehind): bir önceki karakter nokta,
  ünlem ya da soru işaretiyse. Böylece noktalama cümlede kalıyor, yalnızca
  boşluk siliniyor.
- "$4.50" doğru kaldı (noktadan sonra boşluk yok), ama **"Dr."** ayrı bir
  cümle sayıldı. "Mr.", "e.g.", "U.S." da aynı tuzağa düşer.
- Gerçek cümle bölücüler (nltk, spaCy) kısaltma listeleri ya da eğitilmiş
  modeller kullanır. Alıştırmada bir kısaltma listesiyle bunu düzelteceksin.

## Türkçede kesme işareti

```python
import re

print(re.findall(r"\w+", "İstanbul'da 3 gün kaldım."))
```

```text
['İstanbul', 'da', '3', 'gün', 'kaldım']
```

Python 3'te `\w` Unicode'u tanır: "ü", "ı" kelimenin parçası. Kesme işareti
özel adı ekinden ayırıyor: "İstanbul" ve "da" ayrı token. Bu çoğu zaman
istenen sonuçtur: "İstanbul'da", "İstanbul'a", "İstanbul'un" aynı kökü
paylaşıyor. Ama "evlerimizden" gibi kesme işaretsiz eklerde parçalayıcı
yardım etmez; o iş 03. bölümün konusu.

## Özet

- Tokenizasyon metni modelin sayacağı parçalara ayırır; her sonraki adım bu
  kararın üstüne kurulur.
- `split()` noktalamayı kelimeye yapıştırır; `re.findall(r"\w+|[^\w\s]", ...)`
  ayırır ama "can't", tutar ve numaraları dağıtır.
- Kendi desenini yazarken özel kalıpları önce, genel kuralı sona koy;
  `re.VERBOSE` ile açıkla.
- scikit-learn'ün varsayılan deseni tek harfleri ve "n't"yi atar; duygu
  analizinde bunu bil, gerekirse `token_pattern` ver.
- Cümleye bölmek kısaltmalar yüzünden zordur; "Dr." gibi durumlar için liste
  ya da model gerekir.
