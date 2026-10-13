It is tempting to look at attention weights and say "the model looked at
this word and decided from it". But in the lesson the weight was spread out
for "the boy smiled and" and the decision was still right. Let us try
removing words, with the lesson's `attend`:

```python
for prefix in [["the", "queen", "smiled", "and"], ["the", "smiled", "and"],
               ["the", "boy", "smiled", "and"], ["smiled", "and"]]:
    _, a, _, p = attend(prefix)
    print(" ".join(prefix), round(float(p), 3))
```

```text
the queen smiled and 1.0
the smiled and 0.0
the boy smiled and 0.0
smiled and 0.0
```

- Removing "queen" flips the decision from "female" to "male": "queen" really
  makes the decision.
- In a sentence with no person word at all, the decision is "male" too. The
  model learned: "if there is a female word, she; otherwise he". In "the boy
  smiled and", "boy" does not change the decision; the spread-out weights do
  not explain it either.
- The lesson: attention weights show where the model looks, not always **why**
  it decides. Jain and Wallace (2019) showed that in real models different
  attention distributions can give the same decision. The solid way to test
  an explanation is intervention, as here: change the input and see whether
  the decision changes.
