| Belirti | Neden | Çözüm |
|---|---|---|
| `no tests ran`, çıkış kodu `5` | Dosya ya da fonksiyon adı `test_` ile başlamıyor. | `test_cart.py`, `def test_...`. |
| `ModuleNotFoundError: No module named 'cart'` | Testler proje klasörünün dışından çalıştırılıyor. | Proje klasöründe `python -m pytest`. |
| Test hep geçiyor, kod bozukken bile | `assert` yok ya da her zaman doğru bir şey denetleniyor (`assert cart_total`). | Sonucu bir değerle karşılaştır; kodu bozup testin düştüğünü gör. |
| `assert 0.30000000000000004 == 0.3` | Ondalıklı sayılar bilgisayarda tam yazılamaz. | `assert x == pytest.approx(0.3)` ya da `round`. |
| Testler tek tek geçiyor, birlikte düşüyor | Bir test öbürünün bıraktığı duruma (dosya, liste) bağlı. | Her test kendi verisini kendisi hazırlasın. |
| `pytest.raises` testi düşüyor: `DID NOT RAISE` | Kod beklenen hatayı vermiyor. | Kodu düzelt; ya da hata türü yanlış yazılmış. |
| Bende geçiyor, hatta düşüyor | Hatta paket eksik ya da Python sürümü farklı. | `requirements.txt` ve `python-version`. |

**Kural:** bir hatayı düzeltmeden önce o hatayı yakalayan testi yaz. Test
önce düşmeli, düzeltmeden sonra geçmeli; hata bir daha geri gelirse hat
onu yakalar.
