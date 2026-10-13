Bir sistemi iyileştirmenin ilk adımı, hataların **nerede toplandığına**
bakmaktır. Karma arama ilk sonuçta hangi kategorileri karıştırıyor?

```python
import textwrap

best = categories[engine.scores(queries).argmax(axis=1)]
wrong = best != labels
pairs = Counter(zip(labels[wrong], best[wrong]))
print(int(wrong.sum()))
for (truth, guess), n in pairs.most_common(4):
    print(truth, "->", guess, n)
(truth, guess), _ = pairs.most_common(1)[0]
i = next(i for i in range(len(queries))
         if labels[i] == truth and best[i] == guess)
print(textwrap.fill(queries[i], 76))
```

```text
322
shipping -> billing 63
shipping -> refund 38
technical -> account 36
shipping -> technical 26
Dear support, Where is my order ORD-96253? It has not arrived yet. This is
the second time this happens.
```

- 2000 talebin 322'sinde ilk sonuç yanlış. En sık hata kargo taleplerinin
  fatura makalesine gitmesi (63), sonra kargonun iadeye (38) gitmesi.
- Örnek talep açıkça bir kargo sorusu: "Where is my order ...? It has not
  arrived yet." Ama "order" kelimesi fatura makalelerinde de geçiyor ve
  talebin geri kalanı ("dear support", "the second time this happens")
  hiçbir şey söylemiyor. Ortalama vektörde konuyu taşıyan iki kelime,
  konuyla ilgisiz kelimelerin arasında eriyor.
- Buradan çıkan iyileştirme fikirleri: selamlama ve kapanış cümlelerini
  atmak, kelimeleri TF-IDF ağırlığıyla ortalamak (04'teki SIF), ya da her
  kategoriye daha çok makale yazmak. Hangisinin işe yaradığını yine ölçerek
  görmek gerekir: hata analizi fikir verir, kanıt vermez.
