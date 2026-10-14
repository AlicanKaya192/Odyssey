Split the articles in the read-only `doc_data.py` into sentences
(`re.split(r"(?<=\.) ", text)`) and keep every sentence with its article's
`id`. Build a `TfidfVectorizer(stop_words="english")` on the sentences.
`best_doc(question)` should return the article `id` of the sentence with the
highest cosine similarity to the question.

**Expected output:**

```
giftcards
service
```
