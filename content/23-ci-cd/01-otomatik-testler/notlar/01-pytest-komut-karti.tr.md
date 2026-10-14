**Çalıştırmak**

| Komut | Ne yapar |
|---|---|
| `python -m pytest` | Klasördeki bütün testleri bulur ve çalıştırır. |
| `python -m pytest -q` | Kısa çıktı: her test bir nokta, sonda özet. |
| `python -m pytest -v` | Her test ayrı satırda, adıyla. |
| `python -m pytest -x` | İlk düşen testte durur. |
| `python -m pytest -k discount` | Yalnızca adında `discount` geçen testler. |
| `python -m pytest test_cart.py` | Yalnızca bu dosya. |
| `python -m pytest --tb=short` | Hata dökümü kısa. |

`pytest` yerine `python -m pytest` yazmak, testlerin hangi Python'la
çalıştığını açık eder ve proje klasörünü içe aktarma yoluna ekler.

**pytest neyi test sayar**

- Adı `test_` ile başlayan ya da `_test.py` ile biten dosyalar.
- Bu dosyalarda adı `test_` ile başlayan fonksiyonlar.
- Adı `Test` ile başlayan sınıfların `test_` metotları.

**Çıkış kodları**

| Kod | Anlamı | Hatta |
|---|---|---|
| `0` | Bütün testler geçti | Yeşil |
| `1` | En az bir test düştü | Kırmızı |
| `2` | Kullanıcı yarıda kesti | Kırmızı |
| `5` | Hiç test bulunamadı | Kırmızı |

**Yazım kalıpları**

```python
assert sonuc == beklenen

with pytest.raises(ValueError):
    hatali_cagri()

@pytest.mark.parametrize("girdi, beklenen", [(1, 2), (3, 4)])
def test_ornek(girdi, beklenen):
    assert islem(girdi) == beklenen
```
