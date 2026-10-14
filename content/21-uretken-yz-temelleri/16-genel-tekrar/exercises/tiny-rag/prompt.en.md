Split the articles in the read-only `doc_data.py` into sentences
(`re.split(r"(?<=\.) ", text)`) and build a
`TfidfVectorizer(stop_words="english")`. `answer(question)` should return the
sentence with the highest cosine similarity to the question; if the highest
similarity is below 0.25, return `"I could not find this in the sources."`
(09, 10).

**Expected output:**

```
Gift cards are available for
I could not find this
```
