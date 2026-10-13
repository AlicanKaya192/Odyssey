Ön eğitimli vektörler her yerde işe yarar mı? Aynı deneyi, vektörleri bu
kez **ürün yorumlarından** öğrenerek tekrarlayalım ve destek taleplerinde
kullanalım:

```python
from text_data import make_reviews

reviews = [r["text"] for r in make_reviews(20000, seed=1)]
index, E = pretrain(reviews)
words = [w for t in test_texts for w in TOKEN.findall(t.lower())
         if w not in ENGLISH_STOP_WORDS]
print(len(index), round(sum(w in index for w in words) / len(words), 3))
D = np.array([embed(t) for t in texts])
print(curve_point(20), curve_point(50))
```

```text
425 0.134
(0.623, 0.4) (0.749, 0.517)
```

- Yorumlardan öğrenilen 425 kelime, taleplerdeki kelimelerin yalnızca
  %13,4'ünü tanıyor: "refund", "password", "invoice" yorumlarda hiç
  geçmiyor.
- 20 etiketle doğruluk %40, 50 etiketle %51,7. Talep vektörleriyle %74,8 ve
  %86,6 idi; **TF-IDF'in bile gerisinde** (%62,3, %74,9). Yanlış alandan
  gelen ön eğitim yardım etmek bir yana zarar veriyor.
- Gerçek ön eğitimli modeller çok geniş metinle (web, kitaplar, kod)
  eğitildiği için çoğu alanda iş görür; yine de hukuk, tıp, kod gibi özel
  alanlarda o alanın metniyle **ön eğitime devam etmek** (domain-adaptive
  pretraining) belirgin kazanç sağlar.
- Ders: ön eğitimli bir modeli seçmeden önce, kendi metninin kelimelerini ne
  kadar tanıdığına bak.
