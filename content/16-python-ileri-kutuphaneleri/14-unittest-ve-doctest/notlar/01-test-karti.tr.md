## unittest

| Yazım | Ne yapar |
|---|---|
| `class TestX(unittest.TestCase):` | test sınıfı |
| `def test_...(self):` | bir test |
| `def setUp(self):` / `tearDown` | her testten önce / sonra |
| `unittest.main()` | dosyadaki testleri çalıştır |
| `python -m unittest` | klasördeki `test_*.py`'leri bul ve çalıştır |

## assert metotları

| Yazım | Ne zaman düşer |
|---|---|
| `assertEqual(a, b)` | `a != b` |
| `assertTrue(x)` / `assertFalse(x)` | `x` yanlış / doğru |
| `assertIn(a, b)` | `a`, `b`'de yok |
| `assertIsNone(x)` | `x` `None` değil |
| `assertAlmostEqual(a, b)` | 7 ondalıkta farklı |
| `with assertRaises(Hata):` | blokta o hata çıkmadı |
| `with subTest(x=x):` | döngüdeki her değer ayrı rapor |

## unittest.mock

| Yazım | Ne yapar |
|---|---|
| `@patch("modül.ad", return_value=10)` | test süresince adı sahtesiyle değiştir |
| `with patch("modül.ad") as fake:` | aynısı blokla |
| `fake.side_effect = ValueError("x")` | çağrılınca hata versin |
| `fake.call_count` | kaç kez çağrıldı |
| `fake.assert_called_once_with(...)` | bir kez, bu argümanlarla mı |

## doctest

| Yazım | Ne yapar |
|---|---|
| `>>> ifade` + alt satırda sonuç | docstring içinde örnek |
| `doctest.testmod()` | dosyadaki örnekleri dene; `TestResults(failed, attempted)` |
| `python -m doctest dosya.py -v` | komut satırından |
