`remember(memory, text)` belleğin **bir kopyasını** güncelleyip döndürsün
(verilen sözlüğü değiştirme): hazır `FACTS` kalıplarından eşleşen her
biri için değer, kalıpta grup varsa son grup, yoksa bütün eşleşme
(`found.group(found.lastindex or 0)`). Eşleşmeyen anahtara dokunma.

**Beklenen çıktı:**

```
{'name': 'Ada'}
{'name': 'Ada', 'order': 'ORD-48213'}
{'name': 'Ada', 'order': 'ORD-48213'}
```
