# Otomatik Testler

Önceki bölümde hattın her değişiklikte kodu test ettiğini gördük. Ama hat
testleri **yazmaz**, yalnızca çalıştırır. Testi yazmayan bir ekip için CI,
kodun yalnızca kurulabildiğini söyler; doğru çalıştığını söyleyemez. Bu
bölümde Python'un en yaygın test aracı **pytest** ile test yazmayı, düşen
bir testi okumayı ve hattın "geçti / düştü" kararını nasıl verdiğini
görüyoruz.

## Elle denemek neden yetmez

Bir alışveriş sepetinin toplamını hesaplayan bir fonksiyon yazdığını
düşün. Yazdıktan sonra birkaç kez çağırıp sonuca bakarsın; doğruysa devam
edersin. Bu bir testtir, ama **elle** yapılmış bir test:

- Bir hafta sonra fonksiyonu değiştirdiğinde aynı denemeleri yeniden
  yapmayı unutursun.
- Fonksiyonu başka biri değiştirdiğinde hangi durumları denediğini bilmez.
- On fonksiyonun her biri için beşer deneme, her değişiklikte elli deneme
  demek.

**Otomatik test**, o denemeyi bir kez koda dökmek demek: fonksiyonu çağıran
ve sonucun beklenen değer olduğunu **denetleyen** küçük bir fonksiyon. Bir
kez yazılır, istendiği kadar ve saniyeler içinde yeniden çalışır. Hat da
tam olarak bunu yapar: her değişiklikte bütün testleri çalıştırır.

## Test edilecek kod

Örnek olarak bir sepet toplamı alalım. İndirim yüzde olarak veriliyor:

```python
def cart_total(prices, discount=0):
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

Bu kod `cart.py` adlı dosyada duruyor.

## İlk testler

Python'da bir şeyin doğru olduğunu denetlemenin en kısa yolu `assert`
(iddia et) deyimi: `assert koşul` yazarsın, koşul doğruysa hiçbir şey
olmaz, yanlışsa program `AssertionError` hatasıyla durur.

pytest bu deyimin üstüne kurulu. Kuralları basit:

- Test dosyasının adı `test_` ile başlar: `test_cart.py`.
- İçindeki her test bir fonksiyon ve adı da `test_` ile başlar.
- Fonksiyonun içinde test edilen kodu çağırır, sonucu `assert` ile
  denetlersin.

`test_cart.py`:

```python
from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60


def test_total_with_discount():
    assert cart_total([50, 50], discount=20) == 80


def test_empty_cart():
    assert cart_total([]) == 0
```

Her testin adı neyi denediğini söylüyor. Bir test düştüğünde ilk
göreceğin şey bu ad olacak; `test_1` gibi bir ad orada hiçbir şey
anlatmaz.

Testleri çalıştırmak için terminalde proje klasöründe şunu yazarsın:

```text
python -m pytest -q
```

pytest klasördeki `test_` ile başlayan dosyaları kendisi bulur, içlerindeki
`test_` fonksiyonlarını çalıştırır. `-q` (quiet, sessiz) çıktıyı kısa
tutar. Sonuç:

```text
...                                                                      [100%]
3 passed
```

Her nokta (`.`) geçen bir test. Son satır özet. Süre her çalıştırmada
değiştiği için çıktılardan süreyi çıkardık.

## Düşen bir test nasıl okunur

Şimdi biri `cart.py`'de küçük bir yazım hatası yapsın: `100` yerine `10`.

```python
def cart_total(prices, discount=0):
    total = sum(prices)
    if discount:
        total = total - total * discount / 10
    return round(total, 2)
```

Testler değişmedi. Yeniden çalıştırınca (`--tb=short` hata dökümünü kısa
tutar):

```text
.F.                                                                      [100%]
================================== FAILURES ===================================
__________________________ test_total_with_discount ___________________________
test_cart.py:9: in test_total_with_discount
    assert cart_total([50, 50], discount=20) == 80
E   assert -100.0 == 80
E    +  where -100.0 = cart_total([50, 50], discount=20)
=========================== short test summary info ===========================
FAILED test_cart.py::test_total_with_discount - assert -100.0 == 80
1 failed, 2 passed
```

Okuma sırası şu:

1. **Noktalar ve `F`:** ikinci test düşmüş (`F`, failed), öbür ikisi
   geçmiş.
2. **Hangi test:** `test_total_with_discount`. Adı sayesinde sorunun
   indirimde olduğunu daha koda bakmadan anlıyoruz.
3. **Hangi satır ve neden:** `assert -100.0 == 80`. Fonksiyon `80`
   döndürmeliydi, `-100.0` döndürdü.
4. **Özet:** `1 failed, 2 passed`.

İndirimsiz testler geçmeye devam ediyor, çünkü hata yalnızca indirim
dalında. Her durumu ayrı bir testte denemek bu yüzden işe yarıyor: düşen
testin adı sorunun yerini gösteriyor.

## Çıkış kodu: hat kararı nasıl verir

Hat bir testin çıktısını okumaz; komutun **çıkış koduna** (exit code)
bakar. Her program bitince işletim sistemine bir sayı bırakır: `0`
"sorun yok" demek, `0` dışındaki her sayı "bir şey ters gitti" demek.
İş akışındaki `run: python -m pytest` adımı çıkış kodu `0` değilse düşer
ve hat orada durur.

pytest'in çıkış kodları, aynı testleri üç durumda çalıştırarak ölçtük:

```text
all tests pass  -> exit code 0
one test fails  -> exit code 1
no test files   -> exit code 5
```

- `0`: bütün testler geçti → adım yeşil.
- `1`: en az bir test düştü → adım kırmızı.
- `5`: hiç test bulunamadı → adım yine kırmızı. Dosya adını `test_` ile
  başlatmayı unutmak testleri sessizce yok eder; pytest bunu hata sayar,
  iyi ki sayar.

## Hata beklemek: `pytest.raises`

Bazen doğru davranış hata vermektir. Yüzde 150 indirim anlamsız;
fonksiyon bunu sessizce hesaplamak yerine reddetmeli:

```python
def cart_total(prices, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

Hatanın gerçekten verildiğini `pytest.raises` ile denetleriz. `with`
bloğunun içindeki kod o türden bir hata vermezse test düşer:

```python
import pytest

from cart import cart_total


def test_discount_over_100_is_rejected():
    with pytest.raises(ValueError):
        cart_total([10], discount=150)


def test_negative_discount_is_rejected():
    with pytest.raises(ValueError):
        cart_total([10], discount=-5)
```

```text
..                                                                       [100%]
2 passed
```

## Aynı testi birçok girdiyle: `parametrize`

Aynı denetimi beş farklı girdiyle yapmak için beş fonksiyon yazmak
gerekmiyor. `@pytest.mark.parametrize` bir test fonksiyonunu verilen her
girdi satırıyla ayrı ayrı çalıştırır:

```python
import pytest

from cart import cart_total


@pytest.mark.parametrize("prices, discount, expected", [
    ([10, 20], 0, 30),
    ([100], 25, 75),
    ([19.99, 0.01], 50, 10),
    ([], 30, 0),
])
def test_cart_total(prices, discount, expected):
    assert cart_total(prices, discount) == expected
```

İlk metin satırındaki adlar (`prices, discount, expected`) her satırdaki
üç değere sırayla verilir. `-v` (verbose, ayrıntılı) her testi ayrı satırda
gösterir:

```text
============================= test session starts =============================
collecting ... collected 4 items

test_param.py::test_cart_total[prices0-0-30] PASSED                      [ 25%]
test_param.py::test_cart_total[prices1-25-75] PASSED                     [ 50%]
test_param.py::test_cart_total[prices2-50-10] PASSED                     [ 75%]
test_param.py::test_cart_total[prices3-30-0] PASSED                      [100%]

============================== 4 passed ==============================
```

Dört satır, dört ayrı test. Biri düşerse hangi girdide düştüğü köşeli
parantezin içinde yazar.

## İyi bir testin özellikleri

- **Tek davranış.** Bir test tek bir şeyi dener ve adı onu söyler.
- **Hazırla, çalıştır, denetle.** Girdiyi hazırla, kodu çağır, sonucu
  `assert` ile denetle. Üçü de kısa olsun.
- **Sınırları dene.** Boş liste, sıfır, en büyük değer, hatalı girdi.
  Hatalar çoğu zaman sınırlarda saklanır: `<` ile `<=` arasındaki fark gibi.
- **Testin düşebildiğini gör.** Kodu bilerek boz ve testin düştüğünü gör.
  Hiçbir zaman düşmeyen bir test hiçbir şeyi korumaz.
- **Bağımsız ve hızlı.** Testler birbirinin sonucuna bağlı olmasın, hangi
  sırayla çalışırlarsa çalışsınlar aynı sonucu versinler. Hat her
  değişiklikte hepsini çalıştıracak.

## Hatta testler

Önceki bölümdeki iş akışı dosyası şimdi daha anlamlı: `pytest` paketi
`requirements.txt`'te yazılı, kurulum adımı onu kuruyor, son adım testleri
çalıştırıyor ve çıkış koduna göre hat yeşil ya da kırmızı oluyor.

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

`on: [push, pull_request]` iki olayda da çalış demek: kod gönderildiğinde
ve biri birleştirme isteği (pull request) açtığında. Tetikleyicileri
ayrıntısıyla dördüncü bölümde göreceğiz.

## Bu bölümün alıştırmaları

Test alıştırmalarında testleri `main.py`'ye yazıyorsun; test edilen modül
yan sekmede, salt okunur. Odyssey testlerini önce doğru kodda çalıştırır
(hepsi geçmeli), sonra kodun **bilerek bozulmuş** sürümlerinde (her
birinde en az bir testin düşmesi gerekir). Bozuk sürümü yakalayamayan bir
test kümesi eksik demektir; mesaj hangi hatayı kaçırdığını söyler.

## Özet

- Otomatik test, bir denemeyi bir kez koda döker; hat onu her değişiklikte
  çalıştırır.
- pytest `test_` ile başlayan dosya ve fonksiyonları bulur; denetim `assert`
  ile yapılır.
- Düşen test: adı, satırı ve `assert` satırındaki iki değer sorunu gösterir.
- Hat kararı çıkış kodundan verir: `0` yeşil, `1` düştü, `5` test yok.
- `pytest.raises` beklenen hatayı, `parametrize` aynı testi birçok girdiyle
  dener.
