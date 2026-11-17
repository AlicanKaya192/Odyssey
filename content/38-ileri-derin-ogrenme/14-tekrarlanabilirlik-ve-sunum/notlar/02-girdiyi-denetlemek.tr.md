Derslerdeki tahmin fonksiyonu yalnızca uzunluğu denetliyordu. Gerçek
dünyadan gelen girdi çok daha yaratıcıdır: metin, eksik değer, `NaN`, iç içe
liste. Modelin önüne konan bir denetim, hatayı "model saçmaladı" yerine
"girdi yanlıştı" diye adlandırır.

```python
import math


def check_features(values, n=6):
    if not isinstance(values, list) or len(values) != n:
        return f"expected a list of {n} numbers"
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in values):
        return "values must be finite numbers"
    return None


for v in ([1, 2, 3, 4, 5, 6], [1, 2], [1, 2, 3, 4, 5, float("nan")], "abc"):
    print(check_features(v))
```

```text
None
expected a list of 6 numbers
values must be finite numbers
expected a list of 6 numbers
```

- `None`: girdi geçerli. Öbürleri kullanıcıya gösterilebilecek açık mesajlar.
- `math.isfinite` hem `NaN`'ı hem sonsuzu yakalar; `NaN` bir ağdan geçince
  bütün çıkışı `NaN` yapar ve `argmax` sessizce bir sınıf seçer.
- Dikkat: Python'da `True` bir `int`'tir, yani `[True, ...]` bu denetimden
  geçer. Gerekirse `type(v) is bool` ayrıca reddedilir.

## Sunarken başka neler?

- **Aynı ön işleme:** eğitimde veriyi ölçeklediysen (ortalama, standart
  sapma) aynı sayılar modelle birlikte saklanır ve tahminde de uygulanır.
  En sık sunma hatası budur: model doğru, girdi farklı ölçekte.
- **Sürüm:** cevaba modelin sürümünü ekle (`{"label": ..., "model": "1.2"}`);
  bir şikâyet geldiğinde hangi modelin cevap verdiği bilinsin.
- **Toplu istek:** birden çok satırı tek çağrıda kabul etmek, satır satır
  çağırmaktan çok daha hızlıdır (Performans bölümündeki ölçüm).
- **Kayıt:** gelen girdilerin ve cevapların bir kısmını sakla; modelin
  gördüğü verinin zamanla kayıp kaymadığı (veri kayması) ancak böyle
  anlaşılır.
