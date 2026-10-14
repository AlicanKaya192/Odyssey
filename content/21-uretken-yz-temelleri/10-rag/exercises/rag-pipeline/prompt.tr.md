Salt okunur `rag_tools.py` dersteki parçaları içeriyor: `index`,
`build_messages`, `make_reader`. `answer(question, k)` şunları yapsın:
`index.search(question, k)` ile parçaları bul, `build_messages` ile mesajları
kur, `ChatClient([make_reader(2)])` ile `chat(messages, max_tokens=100)`
çağır. Döndür: `[cevap metni, giren token]`.

**Beklenen çıktı:**

```
135
Gift cards are available for 25, 50 and
100 euros and are valid for 3 years. [1]
117
I could not find this in the sources.
```
