Parçalayıcı yazarken en çok kullanılan düzenli ifade parçaları.

## Yapı taşları

| Parça | Anlamı | Örnek eşleşme |
|---|---|---|
| `\w` | harf, rakam, alt çizgi (Unicode) | `a`, `ş`, `7`, `_` |
| `\d` | rakam | `4` |
| `\s` | her türlü boşluk | boşluk, sekme, satır sonu |
| `[^\w\s]` | ne harf ne boşluk: noktalama | `!`, `,`, `$` |
| `+` / `*` / `?` | bir ya da daha çok / sıfır ya da daha çok / isteğe bağlı | `\w+`, `\d*`, `s?` |
| <code>a&#124;b</code> | ya a ya b; soldan sağa denenir | <code>\$\d+&#124;\w+</code> |
| `(?:...)` | yakalamayan grup | `\w+(?:'\w+)?` |
| `(?<=x)` | önünde x olan konum (geriye bakış) | `(?<=[.!?])\s+` |
| `\b` | kelime sınırı | `\bcat\b` |
| `re.VERBOSE` | desende boşluk ve `#` açıklama | uzun desenler |

## Fonksiyonlar

| Fonksiyon | Ne döndürür |
|---|---|
| `re.findall(desen, metin)` | Uyan bütün parçaların listesi (token listesi) |
| `re.split(desen, metin)` | Desenden bölünmüş parçalar (cümle bölme) |
| `re.sub(desen, yeni, metin)` | Uyanların yerine `yeni` (temizlik, yer tutucu) |
| `re.compile(desen)` | Tekrar tekrar kullanılacak desen nesnesi |

## scikit-learn'e kendi desenini vermek

Varsayılan desen tek harfleri ve "n't"yi atıyordu. Kesme işaretli kelimeleri
ve tek harfleri tutan bir desen:

```python
from sklearn.feature_extraction.text import CountVectorizer

keep = CountVectorizer(token_pattern=r"(?u)\b\w+(?:'\w+)?\b").build_analyzer()
print(keep("I can't wait: it's a 5-star deal!"))
```

```text
['i', "can't", 'wait', "it's", 'a', '5', 'star', 'deal']
```

"can't", "it's", "i", "a" ve "5" artık duruyor. Noktalama hâlâ yok:
`token_pattern` yalnızca uyan parçaları alır.

## Sık kullanılan kalıplar

| Kalıp | Desen (yaklaşık) |
|---|---|
| E-posta | `[\w.+-]+@\w+\.\w+` |
| Adres (URL) | `https?://\S+` |
| Etiket ve kullanıcı | `[#@]\w+` |
| Para | `\$\d+(?:[.,]\d+)*` |
| Tarih (gg.aa.yyyy) | `\d{2}\.\d{2}\.\d{4}` |
| Tireli kelime | `\w+(?:-\w+)+` |

Bunlar "yaklaşık": gerçek e-posta ve adres kuralları çok daha karmaşık. Metin
verisinde bu kadarı çoğu zaman yeter; desenini her zaman kendi verinde dene.
