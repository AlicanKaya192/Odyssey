The parts of a RAG prompt:

```text
system: Answer only from the numbered sources. Cite the source number
        like [2]. If the sources do not contain the answer, reply:
        I could not find this in the sources.

user:   Sources:
        [1] Gift cards are available for 25, 50 and 100 euros and are
            valid for 3 years.
        [2] Purchases paid with a gift card are refunded as a new gift card.
        [3] Points expire if you make no purchase for 12 months.

        Question: Do gift cards expire?
```

**Why like this?**

- **The rules are in the system message:** the same in every call, kept apart
  from the user's question.
- **The sources are numbered:** the model can state with a number where the
  answer comes from, and the program can check it (08).
- **The "not found" sentence is written out exactly:** the program can compare
  the answer with it and know that the model abstained.
- **The question comes last:** the model reaches the question after reading
  the sources.

**On the program side:**

1. Clean the question before searching (extra spaces, very long text).
2. Limit the chunks found to the token budget (09).
3. Extract the source numbers from the answer; if a number does not exist or a
   detail does not appear in the source, mark the answer.
4. Show the "not found" answer properly in the interface; direct the user to a
   person or another channel.

**Common mistakes:**

- **Pasting the sources without numbers:** the answer cannot be checked.
- **Leaving the "not found" sentence free:** the model says it differently each
  time and the program cannot tell that it abstained.
- **Too many sources:** tokens rise and unrelated chunks blur the answer.
- **Taking a search error for a model error:** first check whether the right
  chunk got into the prompt.
