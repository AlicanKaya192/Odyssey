What happens with a word never seen in training? Its emission probability is
the same small value for every tag (smoothing), so the word itself says
nothing. The decision is left entirely to the transitions:

```python
for text in ["the zebra was quiet", "they zebra the dog", "a quiet zebra"]:
    print(text, viterbi(text.split()))
```

```text
the zebra was quiet ['DET', 'NOUN', 'VERB', 'ADJ']
they zebra the dog ['PRON', 'VERB', 'DET', 'NOUN']
a quiet zebra ['DET', 'ADJ', 'NOUN']
```

- "zebra" got the noun tag after DET and the verb tag after PRON. The model
  never saw the word but guessed its type from its **position** in the
  sentence.
- People do the same: in "the glorp was quiet" we know "glorp" is a noun.
- Real taggers also look at the **shape** of an unknown word: ending in
  "-ly" is mostly an adverb, "-ing" a verb, a capital letter a proper noun.
  The methods that came after HMMs (conditional random fields, CRF; then
  neural networks) use such features and a longer context together.
