`finish(proposed, max_tokens)` should take the tokens the model would
produce in order (`proposed`) and imitate the generation loop: if `"<end>"`
comes, stop and return `[text, "stop"]`; if the number of generated tokens
reaches `max_tokens`, return `[text, "length"]`. The text is the generated
tokens joined with spaces (`"<end>"` is not part of the text).

**Expected output:**

```
['paris .', 'stop']
['the capital of', 'length']
```
