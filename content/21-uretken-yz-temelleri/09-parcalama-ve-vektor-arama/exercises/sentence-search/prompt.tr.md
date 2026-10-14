Salt okunur `doc_data.py`'deki makaleleri cümlelere böl
(`re.split(r"(?<=\.) ", text)`), her cümleyi makalesinin `id`'siyle tut.
Cümlelerle bir `TfidfVectorizer(stop_words="english")` kur. `best_doc(question)`
soruya kosinüs benzerliği en yüksek cümlenin makale `id`'sini döndürsün.

**Beklenen çıktı:**

```
giftcards
service
```
