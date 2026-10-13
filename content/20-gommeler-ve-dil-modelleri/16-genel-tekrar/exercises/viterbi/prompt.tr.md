`viterbi(words, start, trans, emit)` HMM'de en olası etiket dizisini
bulsun. İlk kelimede puan `log start[t] + log emit[t][kelime]`; sonraki her
kelimede her etiket için en iyi önceki etiketi (`puan + log trans[önceki][t]`)
seç, yayılımı ekle ve geri işaretçiyi sakla. Sonda en iyi etiketten geriye
yürü.

**Beklenen çıktı:**

```
['DET', 'NOUN']
['NOUN', 'DET', 'NOUN']
```
