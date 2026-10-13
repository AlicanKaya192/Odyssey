Aynı tablolarla `viterbi(words)` en olası etiket dizisini döndürsün. Her
etiket için `(en iyi olasılık, o etikete ulaşan yol)` tut; her yeni kelimede
her etiket için önceki etiketlerin en iyisini seç. Sonda en olası yolu
döndür.

**Beklenen çıktı:**

```
['PRON', 'VERB', 'DET', 'NOUN']
['DET', 'NOUN']
```
