Maskenin gerçekten sızıntıyı önlediğini sınayalım: son kelimeyi
değiştirelim ve ilk dört kelimenin çıktısının değişip değişmediğine bakalım.

```python
X2 = (X + Pe).copy()
X2[4] = E[vocab.index("dog")] + Pe[4]
full = np.ones((5, 5), dtype=bool)
print(np.allclose(block(X + Pe, mask)[:4], block(X2, mask)[:4]))
print(np.allclose(block(X + Pe, full)[:4], block(X2, full)[:4]))
```

```text
True
False
```

- Maskeyle ilk dört kelimenin çıktısı son kelimeden etkilenmiyor (`True`).
  Bu yüzden bir cümlenin bütün konumları için "sonraki kelime" kaybı tek
  bir ileri hesapla bulunabilir: 4. konum 5. kelimeyi tahmin ederken onu
  görmemiş olur. RNN'de aynı iş kelime kelime sırayla yapılmak zorundaydı.
- Maskesiz dikkatte her kelime her kelimeyi görüyor (`False`).

Bu iki seçenek transformer'ların iki büyük ailesini ayırır:

- **Kodlayıcı** (encoder) modeller maskesizdir; her kelime iki yanını da
  görür. Cümledeki bazı kelimeler gizlenip tahmin ettirilerek eğitilirler
  (maskeli dil modeli). Sınıflandırma, arama ve etiketleme gibi metni
  **anlama** işlerinde kullanılırlar.
- **Kod çözücü** (decoder) modeller nedensel maskelidir; sonraki kelimeyi
  tahmin ederek eğitilirler ve metin **üretirler**. Bugün sohbet eden büyük
  dil modelleri bu ailedendir.
- İlk transformer ikisini birlikte kullanıyordu: kodlayıcı kaynak cümleyi
  okuyor, kod çözücü çeviriyi kelime kelime üretiyordu.
