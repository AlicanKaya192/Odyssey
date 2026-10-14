`window(history, keep)` geçmişin ilk mesajını (sistem mesajı) her zaman
tutsun ve ardından yalnızca son `keep` mesajı eklesin. `keep` kalan mesaj
sayısından büyükse hepsi gelir.

**Beklenen çıktı:**

```
['S', 'm3', 'm4', 'm5']
['S', 'm0', 'm1', 'm2', 'm3', 'm4', 'm5']
```
