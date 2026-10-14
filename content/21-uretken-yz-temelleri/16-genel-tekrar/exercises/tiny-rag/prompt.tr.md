Salt okunur `doc_data.py`'deki makaleleri cümlelere böl
(`re.split(r"(?<=\.) ", text)`) ve `TfidfVectorizer(stop_words="english")`
kur. `answer(question)` soruya kosinüs benzerliği en yüksek cümleyi
döndürsün; en yüksek benzerlik 0,25'ten küçükse
`"I could not find this in the sources."` döndürsün (09, 10).

**Beklenen çıktı:**

```
Gift cards are available for
I could not find this
```
