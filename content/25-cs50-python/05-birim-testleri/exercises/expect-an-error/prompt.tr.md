İki test yaz. `test_numbers` birkaç sayıyla `square`'in sonucunu denesin (pozitif, negatif, sıfır). `test_str`, `square("cat")`'in `TypeError` verdiğini iddia etsin: `with pytest.raises(TypeError):` bloğunun içinde çağır.

Bozuk sürümlerden biri metin verilince hata vermiyor, metni olduğu gibi döndürüyor; onu yalnızca `test_str` yakalar.
